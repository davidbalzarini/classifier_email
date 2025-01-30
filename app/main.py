from fastapi import FastAPI
from app.controllers import email_controller

app = FastAPI(
    title="Email Classifier API",
    description="This API allows users to classify emails and manage email processing.",
    version="1.0.0",
    contact={
        "name": "David Balzarini pereira",
        "url": "https://aesthetic-sopapillas-1e903b.netlify.app/",
    },
)

app.include_router(email_controller.router)