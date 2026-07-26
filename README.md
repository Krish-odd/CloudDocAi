# CloudDocAI

CloudDocAI is a cloud-based document management system developed using Flask and SQLite. It allows users to securely upload, manage, search, download, and summarize documents using the Groq AI API.

## Features

- User Registration & Login
- Secure Password Hashing
- File Upload
- Search Documents
- Download Documents
- Delete Documents
- AI-Powered Document Summarization

## Technologies Used

- Python
- Flask
- SQLite
- HTML/CSS
- Groq API
- PyPDF2
- python-docx

## Installation

1. Open terminal inside the project folder.

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the Groq API key.

In `config.py`, set:

```python
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

4. Run:

```bash
python app.py
```

5. Open:

```
http://127.0.0.1:5000
```
