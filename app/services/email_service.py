import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from .email_processor import EmailProcessor
from .classifier import classify_email


def get_email_body(msg):
    """
    Extrai o corpo do email, lidando com diferentes formatos (plain text, HTML)
    """
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" not in content_disposition:
                try:
                    if content_type == "text/plain":
                        return part.get_payload(decode=True).decode(errors='replace')
                    elif content_type == "text/html":
                        return part.get_payload(decode=True).decode(errors='replace')
                except Exception as e:
                    print(f"Erro ao decodificar parte do email: {str(e)}")
                    continue
    else:
        try:
            return msg.get_payload(decode=True).decode(errors='replace')
        except Exception as e:
            print(f"Erro ao decodificar email: {str(e)}")
            return ""

    return ""


def read_emails_with_credentials(username, password, limite=50, dias=30):
    """
    Lê emails da caixa de entrada com filtros usando credenciais fornecidas pelo usuário
    Args:
        username: Nome de usuário do email
        password: Senha do email
        limite: Número máximo de emails para retornar
        dias: Buscar emails dos últimos X dias
    """
    imap_server = "imap.gmail.com"

    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(username, password)
        mail.select("inbox")

        # Filtra emails por data
        data = (datetime.now() - timedelta(days=dias)).strftime("%d-%b-%Y")
        criterio_busca = f'(SINCE "{data}")'
        status, messages = mail.search(None, criterio_busca)
        
        email_ids = messages[0].split()
        # Limita quantidade de emails
        email_ids = email_ids[-limite:] if len(email_ids) > limite else email_ids
        
        emails = []
        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
                
            # Extrair o corpo do email
            body = get_email_body(msg)
            
            classification = classify_email(subject)
            
            
            emails.append({
                "subject": subject,
                #"body": body,
                "classification": classification["classification"],
                "response": classification["response"]
            })

        mail.logout()
        
        # Processar emails após leitura
        processor = EmailProcessor()
        processor.process_new_emails(emails)
        
        return emails

    except Exception as e:
        print(f"Erro ao ler emails: {str(e)}")
        raise e