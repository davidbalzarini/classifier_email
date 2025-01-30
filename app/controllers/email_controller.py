from fastapi import HTTPException, File, UploadFile, APIRouter
from ..services.classifier import classify_email
from ..services.email_processor import EmailProcessor
from ..utils.file_processor import extract_emails_from_pdf, extract_emails_from_txt
from ..models.email_model import EmailCredentials
from ..services.email_service import read_emails_with_credentials

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Bem vindo ao classificador de emails!"}

@router.post("/classify", tags=["Email"], summary="This route allows the user to manually compose an email and return its importance rating")
async def classify(email: str):
    classification = classify_email(email)
    return {"classification": classification}

@router.post("/credentials", tags=["Email"], summary="Get emails with credentials", description="""Fetch emails from the inbox using the credentials provided.\n\n
ATTENTION: THIS FEATURE ONLY WORKS WITH GOOGLE EMAIL\n\n
Required parameters:

- **username**: Google email
- **password**: 16-digit app password generated in the Google settings area
- **emails_number**: number of emails (maximum 50 emails)
- **days**: number of days back from the current date (maximum 30 days)""")
async def get_emails_with_credentials(credentials: EmailCredentials):
    try:
        emails = read_emails_with_credentials(credentials.username, credentials.password, credentials.emails_number, credentials.days)
        return {"emails": emails}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/update-file", tags=["Email"], summary="Upload a file and extract emails from it", description="This route allows the user to upload a file in format txt or pdf and extract emails from it")
async def upload_file(file: UploadFile = File(...)):
    try:
        if file.content_type == "application/pdf":
            emails = extract_emails_from_pdf(file)
        elif file.content_type == "text/plain":
            emails = extract_emails_from_txt(file)
        else:
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado")
        processor = EmailProcessor()
        processor.process_new_emails(emails)
        return {"emails": emails}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history", tags=["Email"], summary="Get the history of processed emails", description="This route allows the user to get the history of processed emails and return the classification of each email")
async def get_history():
    processor = EmailProcessor()
    emails = processor.db.get_processed_emails()
    print(len(emails))
    return {
        "emails": [
            {
                "id": email[0],
                "subject": email[1],
                "classification": email[2],
                "processed_date": email[3]
            }
            for email in emails
        ]
    }