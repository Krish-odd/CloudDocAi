from groq import Groq
from PyPDF2 import PdfReader
from docx import Document
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_file,
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import os

from config import (
    SECRET_KEY,
    UPLOAD_FOLDER,
    MAX_CONTENT_LENGTH,
    ALLOWED_EXTENSIONS,
    GROQ_API_KEY,
)

from database import (
    initialize_database,
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_documents,
    search_documents,
    add_document,
    get_document,
    delete_document,
)

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

initialize_database()
client = Groq(api_key=GROQ_API_KEY)

def allowed_file(filename):
    """Check if uploaded file has an allowed extension."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def format_file_size(size):

    if size < 1024:
        return f"{size} B"

    elif size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"

    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MB"

    return f"{size / (1024 * 1024 * 1024):.1f} GB"

def extract_text(filepath):

    extension = filepath.rsplit(".", 1)[1].lower()

    try:

        if extension == "txt":

            with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                return file.read()


        elif extension == "pdf":

            reader = PdfReader(filepath)

            text = ""

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

            return text


        elif extension == "docx":

            document = Document(filepath)

            text = "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
            )

            return text

        return ""

    except Exception as e:

        print(f"Error reading file: {e}")
        return ""

@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if get_user_by_email(email):
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        create_user(
            username,
            email,
            hashed_password,
        )

        flash("Registration successful. Please login.", "success")

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = get_user_by_email(email)

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            flash("Login successful.", "success")

            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "info")

    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search")

    if search:
        rows = search_documents(session["user_id"], search)
    else:
        rows = get_documents(session["user_id"])

    documents = []

    for row in rows:
        document = dict(row)
        document["formatted_size"] = format_file_size(document["file_size"])
        documents.append(document)

    return render_template(
        "dashboard.html",
        documents=documents,
        username=session["username"],
        summary=None,
    )


@app.route("/upload", methods=["POST"])
def upload():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if "document" not in request.files:
        flash("No file selected.", "danger")
        return redirect(url_for("dashboard"))

    file = request.files["document"]

    if file.filename == "":
        flash("Please choose a file.", "danger")
        return redirect(url_for("dashboard"))

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)
        file_size = os.path.getsize(filepath)
        file_type = filename.rsplit(".", 1)[1].upper()

        add_document(
            session["user_id"],
            filename,
            filepath,
            file_type,
            file_size
        )

        flash("File uploaded successfully.", "success")
    else:
        flash("Invalid file type.", "danger")

    return redirect(url_for("dashboard"))


@app.route("/download", methods=["POST"])
def download():

    if "user_id" not in session:
        return redirect(url_for("login"))

    document_ids = request.form.getlist("document_ids")

    if not document_ids:
        flash("Please select at least one document.", "warning")
        return redirect(url_for("dashboard"))

    # For now download the first selected document.
    # Later we can replace this with ZIP download.

    document = get_document(int(document_ids[0]))

    if not document:
        flash("Document not found.", "danger")
        return redirect(url_for("dashboard"))

    return send_file(
        document["filepath"],
        as_attachment=True
    )

@app.route("/delete", methods=["POST"])
def delete():

    if "user_id" not in session:
        return redirect(url_for("login"))

    document_ids = request.form.getlist("document_ids")

    if not document_ids:
        flash("Please select at least one document.", "warning")
        return redirect(url_for("dashboard"))

    deleted_count = 0

    for document_id in document_ids:

        document = get_document(int(document_id))

        if document:

            if os.path.exists(document["filepath"]):
                os.remove(document["filepath"])

            delete_document(int(document_id))
            deleted_count += 1

    flash(f"{deleted_count} document(s) deleted successfully.", "success")

    return redirect(url_for("dashboard"))

@app.route("/summarize", methods=["POST"])
def summarize():

    if "user_id" not in session:
        return redirect(url_for("login"))

    document_ids = request.form.getlist("document_ids")

    if not document_ids:
        flash("Please select at least one document.", "warning")
        return redirect(url_for("dashboard"))

    combined_text = ""

    for document_id in document_ids:

        document = get_document(int(document_id))

        if document:
            combined_text += extract_text(document["filepath"])
            combined_text += "\n\n"

    if not combined_text.strip():
        flash("No readable text found in the selected document(s).", "danger")
        return redirect(url_for("dashboard"))

    # Prevent sending extremely large documents
    combined_text = combined_text[:12000]

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
        You are CloudDocAI, an AI-powered document analysis assistant.

        Your task is to analyze the uploaded document and generate a clear, well-structured summary.

        Rules:
        - Respond in plain text only.
        - Do NOT use Markdown.
        - Do NOT use **, #, _, or backticks.
        - Keep the summary concise but informative.
        - Do not repeat the document word-for-word.
        - If information is missing, simply omit that section.
        - If the document contains very little information, state that politely.

        Use the following format exactly:

        DOCUMENT SUMMARY

        Overview:
        Provide a brief 2-3 sentence overview of the document.

        Key Points:
        - Point 1
        - Point 2
        - Point 3
        - Point 4
        - Point 5

        Important Facts:
        - Mention important names, dates, figures, statistics, or technical details if present.

        Conclusion:
        Provide a short concluding paragraph explaining the overall purpose or outcome of the document.
        """
                },
                {
                    "role": "user",
                    "content": f"Analyze and summarize the following document:\n\n{combined_text}"
                }
            ],
            temperature=0.3,
            max_tokens=500,
        )

        summary = response.choices[0].message.content
        
    except Exception as e:

        summary = f"Error generating summary: {str(e)}"

    rows = get_documents(session["user_id"])

    documents = []

    for row in rows:
        document = dict(row)
        document["formatted_size"] = format_file_size(document["file_size"])
        documents.append(document)

    return render_template(
        "dashboard.html",
        documents=documents,
        username=session["username"],
        summary=summary,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
