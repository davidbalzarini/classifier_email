# API Classificador de Emails

Esta API permite aos usuários classificar emails e gerenciar o processamento de emails. Ela fornece endpoints para buscar emails usando credenciais, fazer upload de arquivos contendo emails, processar uma lista de emails e recuperar o histórico de emails processados.

## Funcionalidades

- Buscar emails da caixa de entrada usando credenciais fornecidas.
- Fazer upload de um arquivo PDF ou TXT contendo emails para serem processados.
- Processar uma lista de emails fornecida no corpo da requisição.
- Recuperar o histórico de emails processados.

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/seuusuario/classificador_de_emails.git
    cd classificador_de_emails
    ```

2. Crie um ambiente virtual e ative-o:
    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```


## Executando o Servidor

1. Inicie o servidor FastAPI:
    ```sh
    uvicorn app.main:app --reload
    ```

2. Abra o navegador e navegue até `http://localhost:8000/docs` para acessar a documentação interativa da API.

## Endpoints da API

### Buscar Emails com Credenciais

- **URL:** `/credentials`
- **Método:** `POST`
- **Descrição:** Busca emails da caixa de entrada usando as credenciais fornecidas.
- **Parâmetros:**
  - `username`: Email do Google
  - `password`: Senha de 16 dígitos gerada na área de configurações do Google
  - `emails_number`: Número de emails (máximo 50 emails)
  - `days`: Número de dias a partir da data atual (máximo 30 dias)

### Fazer Upload de Arquivo

- **URL:** `/upload-file`
- **Método:** `POST`
- **Descrição:** Faz upload de um arquivo PDF ou TXT contendo emails para serem processados.

### Classificar emails

- **URL:** `/cassify`
- **Método:** `POST`
- **Descrição:** Permite que o usuário escreva um email manualmente e retorna a classificação do email

### Obter Histórico de Emails

- **URL:** `/history`
- **Método:** `GET`
- **Descrição:** Retorna o histórico de emails processados e suas classificações.