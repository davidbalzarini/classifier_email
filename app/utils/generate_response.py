from ..models.email_model import EmailRequest
import requests


def generate_response(email_content: str, classification: str) -> str:
    """Envia o conteúdo do e-mail para o modelo DeepSeek via Ollama e retorna uma resposta."""
    ollama_url = "http://localhost:11434/api/generate"

    if classification == "not important":
        payload = {
            "model": "gemma2:2b",
            "prompt": f" responda o email a seguir como se você fosse a pessoa que está recebendo o email:\n\n'{email_content}'",
            "stream": False
        }
    else:
        payload = {
            "model": "gemma2:2b",
            "prompt": f" responda o email a seguir como se você fosse a pessoa que está recebendo o email de forma mais formal e profissional (porém sem explicações quero só a respota ao email):\n\n'{email_content}'",
            "stream": False
        }

    try:
        response = requests.post(ollama_url, json=payload)
        response_data = response.json()
        return response_data.get("response", "Não consegui gerar uma resposta.")
    except Exception as e:
        return f"Erro ao se comunicar com o modelo: {str(e)}"