from fastapi import FastAPI, HTTPException, Request, Path, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
import logging
from jose import JWTError, jwt
from passlib.context import CryptContext

# 1) CONFIGURAÇÃO DE LOGS
logging.basicConfig(
    filename="app.log",
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2) INSTÂNCIA DO FASTAPI
app = FastAPI()

# 3) MIDDLEWARE DE TRATAMENTO GLOBAL DE EXCEÇÕES
@app.exception_handler(Exception)
async def geral_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erro em {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"status": "erro", "message": "Ocorreu um erro interno."}
    )

# 4) ROTA RAIZ
@app.get("/")
def raiz():
    logger.info("Rota raiz acessada")
    return {"mensagem": "SGHSS API está no ar!"}

# Chave e algoritmo
SECRET_KEY = "SUA_CHAVE_SECRETA_AQUI"
ALGORITHM = "HS256"

# Contexto de hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Ponto de obtenção de token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelo de Usuário “fake”
class User(BaseModel):
    username: str
    hashed_password: str
    role: str  # ex: "admin", "medico", "usuario"

# “Banco” de usuários em memória
fake_users_db = {
    "admin": User(
        username="admin",
        hashed_password=pwd_context.hash("1234"),
        role="admin"
    )
}

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, "Credenciais inválidas")
    token = jwt.encode({"sub": user.username, "role": user.role}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# Dependência para pegar usuário atual de qualquer rota
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(401, "Não autenticado")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return user

# Modelo de dados
class Paciente(BaseModel):
    nome: str
    data_nascimento: str  # yyyy-mm-dd
    cpf: str

# "Banco de dados" em memória
db: List[Paciente] = []

# CREATE → POST /pacientes
@app.post("/pacientes", status_code=201)
def criar_paciente(p: Paciente):
    if any(paciente.cpf == p.cpf for paciente in db):
        raise HTTPException(400, "CPF já cadastrado")
    db.append(p)
    return p

# READ → GET /pacientes
@app.get("/pacientes", response_model=List[Paciente])
def listar_pacientes():
    return db

# UPDATE → PUT /pacientes/{cpf}
@app.put("/pacientes/{cpf}", response_model=Paciente)
def atualizar_paciente(cpf: str, atual: Paciente):
    for i, paciente in enumerate(db):
        if paciente.cpf == cpf:
            db[i] = atual
            return atual
    raise HTTPException(404, "Paciente não encontrado")

# DELETE → DELETE /pacientes/{cpf}
@app.delete("/pacientes/{cpf}", status_code=204)
def deletar_paciente(cpf: str):
    for i, paciente in enumerate(db):
        if paciente.cpf == cpf:
            db.pop(i)
            return
    raise HTTPException(404, "Paciente não encontrado")

# Modelo de dados para Consulta
class Consulta(BaseModel):
    paciente_cpf: str      # Relaciona com o CPF do paciente
    data_hora: str         # ex.: "2025-05-20T14:30:00"
    medico: str
    status: str = "agendada"  # status padrão

# "Banco de dados" em memória para Consultas
db_consultas: List[Consulta] = []

from fastapi import Path

# CREATE → POST /consultas
@app.post("/consultas", status_code=201)
def criar_consulta(c: Consulta):
    # Verifica se o paciente existe
    if not any(paciente.cpf == c.paciente_cpf for paciente in db):
        raise HTTPException(400, "CPF do paciente não cadastrado")
    db_consultas.append(c)
    return c

# READ → GET /consultas
@app.get("/consultas", response_model=List[Consulta])
def listar_consultas():
    return db_consultas

# UPDATE → PUT /consultas/{index}
@app.put("/consultas/{index}", response_model=Consulta)
def atualizar_consulta(
    index: int = Path(..., description="Índice da consulta na lista"),
    atual: Consulta = None
):
    if index < 0 or index >= len(db_consultas):
        raise HTTPException(404, "Consulta não encontrada")
    db_consultas[index] = atual
    return atual

# DELETE → DELETE /consultas/{index}
@app.delete("/consultas/{index}", status_code=204)
def deletar_consulta(
    index: int = Path(..., description="Índice da consulta na lista")
):
    if index < 0 or index >= len(db_consultas):
        raise HTTPException(404, "Consulta não encontrada")
    db_consultas.pop(index)
    return

class Profissional(BaseModel):
    nome: str
    funcao: str          # ex: "médico", "enfermeiro", "técnico"
    crm_ou_registro: str # número do conselho ou registro

db_profissionais: List[Profissional] = []

@app.post("/profissionais", status_code=201)
def criar_profissional(p: Profissional):
    if any(x.crm_ou_registro == p.crm_ou_registro for x in db_profissionais):
        raise HTTPException(400, "Registro já cadastrado")
    db_profissionais.append(p)
    return p

# READ
@app.get("/profissionais", response_model=List[Profissional])
def listar_profissionais():
    return db_profissionais

# UPDATE
@app.put("/profissionais/{registro}", response_model=Profissional)
def atualizar_profissional(registro: str, atual: Profissional):
    for i, x in enumerate(db_profissionais):
        if x.crm_ou_registro == registro:
            db_profissionais[i] = atual
            return atual
    raise HTTPException(404, "Profissional não encontrado")

# DELETE
@app.delete("/profissionais/{registro}", status_code=204)
def deletar_profissional(registro: str):
    for i, x in enumerate(db_profissionais):
        if x.crm_ou_registro == registro:
            db_profissionais.pop(i)
            return
    raise HTTPException(404, "Profissional não encontrado")