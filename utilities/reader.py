import os
import docx
import PyPDF2


def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])


def read_pdf(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text


def read_document(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".txt":
        return read_txt(path)

    elif ext == ".docx":
        return read_docx(path)

    elif ext == ".pdf":
        return read_pdf(path)

    else:
        raise ValueError(f"Unsupported file: {path}")
