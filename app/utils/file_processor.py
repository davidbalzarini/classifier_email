import fitz
from fastapi import UploadFile

def extract_emails_from_pdf(file: UploadFile):
    emails = []
    pdf_document = fitz.open(stream=file.file.read(), filetype="pdf")
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        emails.extend(parse_emails_from_text(text))
    return emails

def extract_emails_from_txt(file: UploadFile):
    content = file.file.read().decode("utf-8")
    return parse_emails_from_text(content)

def parse_emails_from_text(text):
    emails = []
    email_lines = text.split("\n")
    subject = None
    body = []

    for line in email_lines:
        if line.startswith("Subject:"):
            if subject and body:
                emails.append({"subject": subject, "body": "\n".join(body)})
            subject = line[len("Subject:"):].strip()
            body = []
        elif line.startswith("Body:"):
            body.append(line[len("Body:"):].strip())
        else:
            body.append(line.strip())

    if subject and body:
        emails.append({"subject": subject, "body": "\n".join(body)})

    return emails