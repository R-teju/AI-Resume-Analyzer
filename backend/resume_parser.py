from PyPDF2 import PdfReader

def extract_resume_text(file):

    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text.lower()