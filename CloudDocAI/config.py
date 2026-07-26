import os

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Folder where uploaded files will be stored
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# SQLite database location
DATABASE = os.path.join(BASE_DIR, "database.db")

# Flask secret key
SECRET_KEY = "CloudDocAI_2026_VT_Project"

# Maximum upload size (16 MB)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    "pdf",
    "doc",
    "docx",
    "txt"
}

# Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
