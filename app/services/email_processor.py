from ..data.database import Database
from datetime import datetime
from .classifier import classify_email

class EmailProcessor:
    def __init__(self):
        self.processed_emails = set()
        self.total_processados = 0
        self.ultima_execucao = None
        self.db = Database()

    def process_new_emails(self, emails):
        try:
            self.ultima_execucao = datetime.now()
            
            emails_to_save = []
            for email in emails:
                email_subject = email["subject"]
                if email_subject not in self.processed_emails:
                    classification = classify_email(email_subject)
                    print(f"Novo email: {email_subject}")
                    print(f"Classificação: {classification}")
                    emails_to_save.append((email_subject, classification))
                    self.processed_emails.add(email_subject)
                    self.total_processados += 1
            
            # Salvar emails em lote no banco de dados
            #self.db.save_emails(emails_to_save)
                    
        except Exception as e:
            print(f"Erro aqui: {str(e)}")