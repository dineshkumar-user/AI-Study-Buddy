from PyPDF2 import PdfReader
from docx import Document


def read_txt(uploaded_file):
    return uploaded_file.read().decode(
        "utf-8",
        errors="ignore"
    )


def read_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def read_docx(uploaded_file):
    document = Document(uploaded_file)

    text = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)

    return "\n".join(text)


def extract_text(uploaded_file):

    filename = uploaded_file.name.lower()

    if filename.endswith(".txt"):
        return read_txt(uploaded_file)

    if filename.endswith(".pdf"):
        return read_pdf(uploaded_file)

    if filename.endswith(".docx"):
        return read_docx(uploaded_file)

    return ""