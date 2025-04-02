from fastapi import FastAPI
from app.controllers import email_controller
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Email Classifier API",
    description="This API allows users to classify emails and manage email processing.",
    version="1.0.0",
    contact={
        "name": "David Balzarini pereira",
        "url": "https://aesthetic-sopapillas-1e903b.netlify.app/",
    },
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_controller.router)