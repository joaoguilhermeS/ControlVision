from fastapi import FastAPI, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn
import os
from fastapi.openapi.utils import get_openapi
from cryptography.fernet import Fernet
import jwt
import jwt
import aiomysql
import asyncio
from dotenv import load_dotenv
from datetime import datetime
from cryptography.fernet import Fernet, InvalidToken
import jwt
from typing import List, Optional
from pydantic import BaseModel
import math
from fastapi.responses import StreamingResponse
from openai import OpenAI
import requests
import json

class Usuario(BaseModel):
    matricula: int
    nome: str
    senha: str
    usuario: str
    cpf: int

class InfoProdutividade(BaseModel):
    id: int
    data_produtividade: datetime
    lista_de_produtividade: str
    matricula: int

class Observacoes(BaseModel):
    id: int
    data_observacoes: datetime
    conteudo: str
    matricula: int

class Producao(BaseModel):
    id: int
    tipo: int
    data_producao: datetime
    quantidade: int
    matricula: int

class VPS(BaseModel):
    ip: str
    root_senha: str
    id_rsa: str

class Manutencao(BaseModel):
    id: int
    data_de_manuntencao: datetime
    descricao: str
    id_rsa: str

class Desenvolvedor(BaseModel):
    id_rsa: str
    matricula: int

class Dispositivos(BaseModel):
    id: int
    thresholds: int
    nome: str
    matricula: int

class Camera(BaseModel):
    id: int
    ip: str
    id_ext: int

class Sensor(BaseModel):
    id: int
    ip: str
    unidade: str
    valor: float
    id_ext: int

class Alarme(BaseModel):
    id: int
    data_do_alarme: datetime
    tipo: str
    texto: str
    id_dispositivo: int


client = OpenAI(api_key='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')


number_of_workers = int(os.environ.get("N_WORKERS", 1))

app = FastAPI()


def custom_openapi():
    # Generate a Fernet key from the provided string (not secure, just for example)
    fernet_key = b'R1sK' * 8  # Fernet keys are 32 url-safe base64-encoded bytes
    fernet = Fernet(fernet_key)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API - ControlVision",
        version="0.1",
        description="Página de API do projeto Control Vision (Sistema de Monitoramento de Ambiente Fabril).",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_database = os.getenv("DB_DATABASE")
fernet_key = os.getenv("FERNET_KEY").encode()
fernet = Fernet(fernet_key)

def encrypt_password(password: str) -> str:
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password: str) -> str:
    try:
        return fernet.decrypt(encrypted_password.encode()).decode()
    except InvalidToken:
        raise HTTPException(status_code=400, detail="Invalid encryption token")

@app.post("/create-usuario")
async def create_usuario(
    matricula: str = Form(...),
    nome: str = Form(...),
    senha: str = Form(...),
    usuario: str = Form(...),
    cpf: int = Form(...)
):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        encrypted_senha = encrypt_password(senha)
        await cursor.execute("INSERT INTO USUARIO (matricula, nome, senha, usuario, cpf) VALUES (%s, %s, %s, %s, %s)", (matricula, nome, encrypted_senha, usuario, cpf))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"message": "Usuario created successfully!"}

@app.put("/update-usuario/{matricula}")
async def update_usuario(matricula: int, nome: str = Form(...), senha: str = Form(...), usuario: str = Form(...), cpf: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        encrypted_senha = encrypt_password(senha)
        await cursor.execute("UPDATE USUARIO SET nome=%s, senha=%s, usuario=%s, cpf=%s WHERE matricula=%s", (nome, encrypted_senha, usuario, cpf, matricula))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Usuario updated successfully!"}

@app.delete("/delete-usuario/{matricula}")
async def delete_usuario(matricula: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("DELETE FROM USUARIO WHERE matricula=%s", (matricula,))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Usuario deleted successfully!"}


@app.post("/create-info-produtividade")
async def create_info_produtividade(data_produtividade: datetime = Form(...), lista_de_produtividade: str = Form(...), matricula: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("INSERT INTO INFO_PRODUTIVIDADE (data_produtividade, lista_de_produtividade, matricula) VALUES (%s, %s, %s)", (data_produtividade, lista_de_produtividade, matricula))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "InfoProdutividade created successfully!"}

@app.put("/update-info-produtividade/{id}")
async def update_info_produtividade(id: int, data_produtividade: datetime = Form(...), lista_de_produtividade: str = Form(...), matricula: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("UPDATE INFO_PRODUTIVIDADE SET data_produtividade=%s, lista_de_produtividade=%s, matricula=%s WHERE id=%s", (data_produtividade, lista_de_produtividade, matricula, id))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "InfoProdutividade updated successfully!"}

@app.delete("/delete-info-produtividade/{id}")
async def delete_info_produtividade(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("DELETE FROM INFO_PRODUTIVIDADE WHERE id=%s", (id,))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "InfoProdutividade deleted successfully!"}

@app.post("/create-observacoes")
async def create_observacoes(data_observacoes: datetime = Form(...), conteudo: str = Form(...), matricula: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("INSERT INTO OBSERVACOES (data_observacoes, conteudo, matricula) VALUES (%s, %s, %s)", (data_observacoes, conteudo, matricula))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Observacoes created successfully!"}

@app.put("/update-observacoes/{id}")
async def update_observacoes(id: int, data_observacoes: datetime = Form(...), conteudo: str = Form(...), matricula: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("UPDATE OBSERVACOES SET data_observacoes=%s, conteudo=%s, matricula=%s WHERE id=%s", (data_observacoes, conteudo, matricula, id))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Observacoes updated successfully!"}

@app.delete("/delete-observacoes/{id}")
async def delete_observacoes(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("DELETE FROM OBSERVACOES WHERE id=%s", (id,))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Observacoes deleted successfully!"}

@app.post("/create-producao")
async def create_producao(tipo: int = Form(...), data_producao: datetime = Form(...), quantidade: int = Form(...), matricula: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("INSERT INTO PRODUCAO (tipo, data_producao, quantidade, matricula) VALUES (%s, %s, %s, %s)", (tipo, data_producao, quantidade, matricula))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Producao created successfully!"}

@app.put("/update-producao/{id}")
async def update_producao(id: int, tipo: int = Form(...), data_producao: datetime = Form(...), quantidade: int = Form(...), matricula: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("UPDATE PRODUCAO SET tipo=%s, data_producao=%s, quantidade=%s, matricula=%s WHERE id=%s", (tipo, data_producao, quantidade, matricula, id))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Producao updated successfully!"}

@app.delete("/delete-producao/{id}")
async def delete_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("DELETE FROM PRODUCAO WHERE id=%s", (id,))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Producao deleted successfully!"}
@app.post("/create-vps")
async def create_vps(ip: str = Form(...), root_senha: str = Form(...), id_rsa: str = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("INSERT INTO VPS (ip, root_senha, id_rsa) VALUES (%s, %s, %s)", (ip, root_senha, id_rsa))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "VPS created successfully!"}

@app.put("/update-vps/{ip}")
async def update_vps(ip: str, root_senha: str = Form(...), id_rsa: str = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("UPDATE VPS SET root_senha=%s, id_rsa=%s WHERE ip=%s", (root_senha, id_rsa, ip))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "VPS updated successfully!"}

@app.delete("/delete-vps/{ip}")
async def delete_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("DELETE FROM VPS WHERE ip=%s", (ip,))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "VPS deleted successfully!"}
@app.post("/create-manutencao")
async def create_manutencao(data_de_manuntencao: datetime = Form(...), descricao: str = Form(...), id_rsa: str = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("INSERT INTO MANUTENCAO (data_de_manuntencao, descricao, id_rsa) VALUES (%s, %s, %s)", (data_de_manuntencao, descricao, id_rsa))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Manutencao created successfully!"}

@app.put("/update-manutencao/{id}")
async def update_manutencao(id: int, data_de_manuntencao: datetime = Form(...), descricao: str = Form(...), id_rsa: str = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("UPDATE MANUTENCAO SET data_de_manuntencao=%s, descricao=%s, id_rsa=%s WHERE id=%s", (data_de_manuntencao, descricao, id_rsa, id))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Manutencao updated successfully!"}

@app.delete("/delete-manutencao/{id}")
async def delete_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("DELETE FROM MANUTENCAO WHERE id=%s", (id,))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Manutencao deleted successfully!"}
@app.post("/create-desenvolvedor")
async def create_desenvolvedor(id_rsa: str = Form(...), matricula: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("INSERT INTO DESENVOLVEDOR (id_rsa, matricula) VALUES (%s, %s)", (id_rsa, matricula))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Desenvolvedor created successfully!"}

@app.put("/update-desenvolvedor/{id_rsa}")
async def update_desenvolvedor(id_rsa: str, matricula: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("UPDATE DESENVOLVEDOR SET matricula=%s WHERE id_rsa=%s", (matricula, id_rsa))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Desenvolvedor updated successfully!"}

@app.delete("/delete-desenvolvedor/{id_rsa}")
async def delete_desenvolvedor(id_rsa: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("DELETE FROM DESENVOLVEDOR WHERE id_rsa=%s", (id_rsa,))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Desenvolvedor deleted successfully!"}
@app.post("/create-dispositivos")
async def create_dispositivos(thresholds: int = Form(...), nome: str = Form(...), matricula: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("INSERT INTO DISPOSITIVOS (thresholds, nome, matricula) VALUES (%s, %s, %s)", (thresholds, nome, matricula))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Dispositivo created successfully!"}

@app.put("/update-dispositivos/{id}")
async def update_dispositivos(id: int, thresholds: int = Form(...), nome: str = Form(...), matricula: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("UPDATE DISPOSITIVOS SET thresholds=%s, nome=%s, matricula=%s WHERE id=%s", (thresholds, nome, matricula, id))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Dispositivo updated successfully!"}

@app.delete("/delete-dispositivos/{id}")
async def delete_dispositivos(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("DELETE FROM DISPOSITIVOS WHERE id=%s", (id,))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Dispositivo deleted successfully!"}
@app.post("/create-camera")
async def create_camera(ip: str = Form(...), id_ext: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("INSERT INTO CAMERA (ip, id_ext) VALUES (%s, %s)", (ip, id_ext))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Camera created successfully!"}

@app.put("/update-camera/{id}")
async def update_camera(id: int, ip: str = Form(...), id_ext: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("UPDATE CAMERA SET ip=%s, id_ext=%s WHERE id=%s", (ip, id_ext, id))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Camera updated successfully!"}

@app.delete("/delete-camera/{id}")
async def delete_camera(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("DELETE FROM CAMERA WHERE id=%s", (id,))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Camera deleted successfully!"}
@app.post("/create-sensor")
async def create_sensor(ip: str = Form(...), unidade: str = Form(...), valor: float = Form(...), id_ext: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("INSERT INTO SENSOR (ip, unidade, valor, id_ext) VALUES (%s, %s, %s, %s)", (ip, unidade, valor, id_ext))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Sensor created successfully!"}

@app.put("/update-sensor/{id}")
async def update_sensor(id: int, ip: str = Form(...), unidade: str = Form(...), valor: float = Form(...), id_ext: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("UPDATE SENSOR SET ip=%s, unidade=%s, valor=%s, id_ext=%s WHERE id=%s", (ip, unidade, valor, id_ext, id))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Sensor updated successfully!"}

@app.delete("/delete-sensor/{id}")
async def delete_sensor(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("DELETE FROM SENSOR WHERE id=%s", (id,))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Sensor deleted successfully!"}
@app.post("/create-alarme")
async def create_alarme(data_do_alarme: datetime = Form(...), tipo: str = Form(...), texto: str = Form(...), id_dispositivo: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("INSERT INTO ALARME (data_do_alarme, tipo, texto, id_dispositivo) VALUES (%s, %s, %s, %s)", (data_do_alarme, tipo, texto, id_dispositivo))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Alarme created successfully!"}

@app.put("/update-alarme/{id}")
async def update_alarme(id: int, data_do_alarme: datetime = Form(...), tipo: str = Form(...), texto: str = Form(...), id_dispositivo: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("UPDATE ALARME SET data_do_alarme=%s, tipo=%s, texto=%s, id_dispositivo=%s WHERE id=%s", (data_do_alarme, tipo, texto, id_dispositivo, id))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Alarme updated successfully!"}

@app.delete("/delete-alarme/{id}")
async def delete_alarme(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("DELETE FROM ALARME WHERE id=%s", (id,))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividade", response_model=List[InfoProdutividade])
async def get_info_produtividade():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/desenvolvedor", response_model=List[Desenvolvedor])
async def get_desenvolvedor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/camera", response_model=List[Camera])
async def get_camera():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensor", response_model=List[Sensor])
async def get_sensor():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarme", response_model=List[Alarme])
async def get_alarme():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Alarme deleted successfully!"}

if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, host='0.0.0.0', reload=True, workers=1, proxy_headers=True)
@app.get("/usuarios/{matricula}", response_model=Usuario)
async def get_usuario(matricula: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM USUARIO WHERE matricula = %s", (matricula,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info-produtividades/{id}", response_model=InfoProdutividade)
async def get_info_produtividade(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/observacoes/{id}", response_model=Observacoes)
async def get_observacao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.get("/producao/{id}", response_model=Producao)
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vps/{ip}", response_model=VPS)
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM VPS WHERE ip = %s", (ip,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/manutencao/{id}", response_model=Manutencao)
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.get("/desenvolvedores/{id_rsa}", response_model=Desenvolvedor)
async def get_desenvolvedor(id_rsa: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa = %s", (id_rsa,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dispositivos/{id}", response_model=Dispositivos)
async def get_dispositivo(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/cameras/{id}", response_model=Camera)
async def get_camera(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM CAMERA WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.get("/sensores/{id}", response_model=Sensor)
async def get_sensor(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM SENSOR WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alarmes/{id}", response_model=Alarme)
async def get_alarme(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor(aiomysql.DictCursor)
        await cursor.execute("SELECT * FROM ALARME WHERE id = %s", (id,))
        result = await cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
