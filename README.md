# CloudDocAI

CloudDocAI is a cloud-based document management system developed using Flask and SQLite. It enables users to securely upload, organize, search, download, and summarize documents with the help of the Groq AI API.

---

## Features

- User Registration and Login
- Secure Password Hashing
- File Upload (PDF, DOC, DOCX, TXT)
- Search Documents
- Download Documents
- Delete Documents
- AI-Powered Document Summarization
- Responsive User Interface

---

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- Groq API
- PyPDF2
- python-docx
- Gunicorn

---

## Project Structure

```
CloudDocAI/
│
├── static/
│   └── css/
├── templates/
├── uploads/
├── app.py
├── config.py
├── database.py
├── database.db
├── requirements.txt
├── runtime.txt
├── Procfile
└── README.md
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Krish-odd/CloudDocAi.git
cd CloudDocAi
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Groq API Key

#### Windows PowerShell

```powershell
$env:GROQ_API_KEY="YOUR_GROQ_API_KEY"
```

#### Windows Command Prompt

```cmd
set GROQ_API_KEY=YOUR_GROQ_API_KEY
```

#### Linux / macOS

```bash
export GROQ_API_KEY="YOUR_GROQ_API_KEY"
```

### 4. Run the Application

```bash
python app.py
```

### 5. Open in Browser

```
http://127.0.0.1:5000
```

---

## Deployment

The project is configured for deployment on **Render**.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn app:app
```

### Environment Variable

Add the following environment variable in your Render dashboard:

```
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

---

## Supported File Types

- PDF (.pdf)
- Microsoft Word (.doc)
- Microsoft Word (.docx)
- Text (.txt)

---

## Security Features

- Passwords are securely hashed before storage.
- User authentication with Flask sessions.
- File names are sanitized before upload.
- API keys are managed through environment variables.

---

## Note

This project uses SQLite for the database and stores uploaded files on the local filesystem.

When deployed on free cloud hosting platforms such as Render, uploaded files and the SQLite database may not persist after a service restart because the filesystem is temporary.

---

## Future Enhancements

- ZIP download for multiple files
- File preview
- User profile management
- Cloud file storage (AWS S3 or Cloudinary)
- PostgreSQL database support
- OCR support for scanned PDFs

---

## Author

**Krish**

Vocational Training Project (2026)
