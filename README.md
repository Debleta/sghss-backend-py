SGHSS API - Sistema de Gestão Hospitalar Simplificado

📝 Descrição
A SGHSS API é um sistema de gestão hospitalar simplificado desenvolvido com FastAPI que permite o gerenciamento de:
Pacientes
Consultas médicas
Profissionais de saúde

A API inclui autenticação via JWT (JSON Web Tokens) e registro de logs para monitoramento de atividades.

🔧 Pré-requisitos
Python 3.7+
FastAPI
Uvicorn (ou outro servidor ASGI)
Bibliotecas listadas em requirements.txt

🚀 Instalação
Clone o repositório:
bash
git clone (https://github.com/Debleta/sghss-backend-py)
cd sghss-api
Crie um ambiente virtual (recomendado):

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Instale as dependências:

bash
pip install -r requirements.txt
⚙️ Configuração
Configure sua chave secreta no arquivo main.py:

python
SECRET_KEY = "SUA_CHAVE_SECRETA_AQUI"  # Substitua por uma chave segura
Os logs são gravados automaticamente no arquivo app.log

🏃 Executando a API
bash
uvicorn main:app --reload

A API estará disponível em: http://127.0.0.1:8000
Documentação interativa: http://127.0.0.1:8000/docs

🔐 Autenticação
A API usa OAuth2 com JWT para autenticação. 
Para obter um token:
Faça uma requisição POST para /token com:

json
{
  "username": "admin",
  "password": "1234"
}
Use o token retornado no cabeçalho das requisições:

Authorization: Bearer <token>
Usuário padrão:

Username: admin
Password: 1234

📊 Endpoints

👥 Pacientes
POST /pacientes - Cadastra um novo paciente
GET /pacientes - Lista todos os pacientes
PUT /pacientes/{cpf} - Atualiza um paciente pelo CPF
DELETE /pacientes/{cpf} - Remove um paciente pelo CPF

🏥 Consultas
POST /consultas - Agenda uma nova consulta
GET /consultas - Lista todas as consultas
PUT /consultas/{index} - Atualiza uma consulta pelo índice
DELETE /consultas/{index} - Remove uma consulta pelo índice

👨‍⚕️ Profissionais
POST /profissionais - Cadastra um novo profissional
GET /profissionais - Lista todos os profissionais
PUT /profissionais/{registro} - Atualiza um profissional pelo registro
DELETE /profissionais/{registro} - Remove um profissional pelo registro

📋 Modelos de Dados
Paciente
json
{
  "nome": "string",
  "data_nascimento": "string (yyyy-mm-dd)",
  "cpf": "string"
}

Consulta
json
{
  "paciente_cpf": "string",
  "data_hora": "string (ISO 8601)",
  "medico": "string",
  "status": "string"
}

Profissional
json
{
  "nome": "string",
  "funcao": "string",
  "crm_ou_registro": "string"
}

📜 Logs
A aplicação registra automaticamente:
Acesso às rotas.
Erros e exceções.
Operações críticas.

Os logs são gravados no arquivo app.log no formato:
TIMESTAMP LEVEL: MESSAGE


⚠️ Limitações
Dados armazenados em memória (não persistente).
Autenticação básica com usuário único.
Sem validação avançada de CPF/datas.

🔄 Melhorias Futuras
Persistência em banco de dados.
Validação de CPF e datas.
Sistema de permissões mais robusto.
Paginação nas listagens.
Testes automatizados.

🧑‍💻 Desenvolvido por Débora Cavalcante de Souza
