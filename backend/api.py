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
from datetime import date
from fastapi import FastAPI, HTTPException
import aiomysql
from datetime import date, datetime
import random

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
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "VPS deleted successfully!"}
@app.post("/create-manutencao")
async def create_manutencao(data_de_manuntencao: datetime = Form(...), descricao: str = Form(...), tipo: int = Form(...), id_rsa: str = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("INSERT INTO MANUTENCAO (data_de_manuntencao, descricao, tipo, id_rsa) VALUES (%s, %s, %s, %s)", (data_de_manuntencao, descricao, tipo, id_rsa))
        await conn.commit()
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
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Camera deleted successfully!"}
@app.post("/create-sensor")
async def create_sensor(ip: str = Form(...), unidade: str = Form(...), id_ext: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("INSERT INTO SENSOR (ip, unidade, valor, id_ext) VALUES (%s, %s, %s, %s)", (ip, unidade, 0, id_ext))
        await conn.commit()
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
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Sensor deleted successfully!"}
@app.post("/create-alarme")
async def create_alarme(alarme_data: dict):
    data_do_alarme = alarme_data['data_do_alarme']
    tipo = alarme_data['tipo']
    texto = alarme_data['texto']
    id_dispositivo = alarme_data['id_dispositivo']
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("INSERT INTO ALARME (data_do_alarme, tipo, texto, id_dispositivo) VALUES (%s, %s, %s, %s)", (data_do_alarme, tipo, texto, id_dispositivo))
        await conn.commit()
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
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()
    return {"message": "Alarme deleted successfully!"}

@app.get("/get-usuario/{matricula}")
async def get_usuario(matricula: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM USUARIO WHERE matricula=%s", (matricula,))
        usuario = await cursor.fetchone()
        if usuario:
            return {"matricula": usuario[0], "nome": usuario[1], "senha": usuario[2], "usuario": usuario[3], "cpf": usuario[4]}
        else:
            raise HTTPException(status_code=404, detail="Usuario not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()

@app.get("/get-info-produtividade/{id}")
async def get_info_produtividade(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM INFO_PRODUTIVIDADE WHERE id=%s", (id,))
        info_produtividade = await cursor.fetchone()
        if info_produtividade:
            return {"id": info_produtividade[0], "data_produtividade": info_produtividade[1], "lista_de_produtividade": info_produtividade[2], "matricula": info_produtividade[3]}
        else:
            raise HTTPException(status_code=404, detail="InfoProdutividade not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()

@app.get("/get-observacoes/{id}")
async def get_observacoes(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM OBSERVACOES WHERE id=%s", (id,))
        observacoes = await cursor.fetchone()
        if observacoes:
            return {"id": observacoes[0], "data_observacoes": observacoes[1], "conteudo": observacoes[2], "matricula": observacoes[3]}
        else:
            raise HTTPException(status_code=404, detail="Observacoes not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()

@app.get("/get-producao/{id}")
async def get_producao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM PRODUCAO WHERE id=%s", (id,))
        producao = await cursor.fetchone()
        if producao:
            return {"id": producao[0], "tipo": producao[1], "data_producao": producao[2], "quantidade": producao[3], "matricula": producao[4]}
        else:
            raise HTTPException(status_code=404, detail="Producao not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()

@app.get("/get-vps/{ip}")
async def get_vps(ip: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM VPS WHERE ip=%s", (ip,))
        vps = await cursor.fetchone()
        if vps:
            return {"ip": vps[0], "root_senha": vps[1], "id_rsa": vps[2]}
        else:
            raise HTTPException(status_code=404, detail="VPS not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()

@app.get("/get-manutencao/{id}")
async def get_manutencao(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM MANUTENCAO WHERE id=%s", (id,))
        manutencao = await cursor.fetchone()
        if manutencao:
            return {"id": manutencao[0], "data_de_manuntencao": manutencao[1], "descricao": manutencao[2], "id_rsa": manutencao[3]}
        else:
            raise HTTPException(status_code=404, detail="Manutencao not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()

@app.get("/get-desenvolvedor/{id_rsa}")
async def get_desenvolvedor(id_rsa: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM DESENVOLVEDOR WHERE id_rsa=%s", (id_rsa,))
        desenvolvedor = await cursor.fetchone()
        if desenvolvedor:
            return {"id_rsa": desenvolvedor[0], "matricula": desenvolvedor[1]}
        else:
            raise HTTPException(status_code=404, detail="Desenvolvedor not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()

@app.get("/get-dispositivos/{id}")
async def get_dispositivos(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM DISPOSITIVOS WHERE id=%s", (id,))
        dispositivos = await cursor.fetchone()
        if dispositivos:
            return {"id": dispositivos[0], "thresholds": dispositivos[1], "nome": dispositivos[2], "matricula": dispositivos[3]}
        else:
            raise HTTPException(status_code=404, detail="Dispositivos not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()

@app.get("/get-camera/{id}")
async def get_camera(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM CAMERA WHERE id=%s", (id,))
        camera = await cursor.fetchone()
        if camera:
            return {"id": camera[0], "ip": camera[1], "id_ext": camera[2]}
        else:
            raise HTTPException(status_code=404, detail="Camera not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()

@app.get("/get-sensor/{id}")
async def get_sensor(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM SENSOR WHERE id=%s", (id,))
        sensor = await cursor.fetchone()
        if sensor:
            return {"id": sensor[0], "ip": sensor[1], "unidade": sensor[2], "valor": sensor[3], "id_ext": sensor[4]}
        else:
            raise HTTPException(status_code=404, detail="Sensor not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()

@app.get("/get-alarme/{id}")
async def get_alarme(id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM ALARME WHERE id=%s", (id,))
        alarme = await cursor.fetchone()
        if alarme:
            return {"id": alarme[0], "data_do_alarme": alarme[1], "tipo": alarme[2], "texto": alarme[3], "id_dispositivo": alarme[4]}
        else:
            raise HTTPException(status_code=404, detail="Alarme not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if cursor:
    #         await cursor.close()
    #     if conn:
    #         await conn.close()

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    conn = None
    cursor = None
    print("oi")
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("SELECT senha FROM USUARIO WHERE usuario=%s", (username,))
        print("antes...")
        result = await cursor.fetchone()
        print(f"result = {result}")
        if (1):
            stored_password_encrypted = result[0]
            stored_password = decrypt_password(stored_password_encrypted)
            print(f"stored_password = {stored_password}")
            if password == stored_password:
                return {"success": True, "message": "Login successful"}
            else:
                return {"success": False, "message": "Invalid password"}
        else:
            return {"success": False, "message": "User not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-all-alarmes")
async def get_all_alarmes():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        today = date.today()
        await cursor.execute("SELECT * FROM ALARME WHERE DATE(data_do_alarme) = %s", (today,))
        alarmes = await cursor.fetchall()
        return {"alarmes": alarmes}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get-all-observacoes")
async def get_all_observacoes():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM OBSERVACOES")
        observacoes = await cursor.fetchall()
        return {"observacoes": observacoes}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get-todays-production-sum-per-user")
async def get_todays_production_sum_per_user():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        # Update the SQL query to include the required columns in the GROUP BY clause or remove unnecessary columns
        await cursor.execute("""
            SELECT USUARIO.nome, SUM(PRODUCAO.quantidade) as total_producao
            FROM PRODUCAO
            JOIN USUARIO ON PRODUCAO.matricula = USUARIO.matricula
            WHERE DATE(PRODUCAO.data_producao) = CURDATE()
            GROUP BY USUARIO.nome
        """)
        production_sums = await cursor.fetchall()
        # Map the results to a dictionary using the user's name as the key
        result = {nome: total for nome, total in production_sums}
        return {"production_sums": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get-todays-production-sum-per-item")
async def get_todays_production_sum_per_item():
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("SELECT tipo, quantidade, data_producao FROM PRODUCAO")
        raw_data = await cursor.fetchall()
        print(f"raw_data = {raw_data}")
        today = date.today()
        filtered_data = [data for data in raw_data if data[2].date() == today]
        production_sums = {}
        for tipo, quantidade, _ in filtered_data:
            if tipo in production_sums:
                production_sums[tipo] += quantidade
            else:
                production_sums[tipo] = quantidade
        return {"production_sums": production_sums}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

temperatura = 0

@app.post("/set-temperatura")
async def set_current_temperatura(payload: dict):
    try:
        global temperatura
        temperatura = int(payload['temperatura'])
        await check_and_create_alarme(temperatura)
    except:
        temperatura = random.randint(18, 30) 

@app.get("/get-temperatura")
async def get_current_temperatura() -> dict:
    global temperatura
    return {"temperatura": temperatura}

optico = 0

@app.post("/set-optico")
async def set_current_optico(payload: dict):
    try:
        global optico
        optico = int(payload['optico'])
    except:
        optico = random.randint(18, 30) 

@app.get("/get-optico")
async def get_current_optico() -> dict:
    global optico
    return {"optico": optico}    

async def check_and_create_alarme(temperatura):
    tipo = None
    if 25 < temperatura < 30:
        tipo = '3'
    elif 33 <= temperatura < 37:
        tipo = '2'
    elif temperatura >= 40:
        tipo = '1'

    if tipo:
        await create_alarme({
            'data_do_alarme': datetime.now(),
            'tipo': tipo,
            'texto': f'Temperatura crítica: {temperatura}°C',
            'id_dispositivo': 1 
        })

@app.get("/get-all-manutencoes")
async def get_all_manutencoes():
    conn = None
    cursor = None   
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("SELECT id, data_de_manuntencao, descricao, tipo, id_rsa FROM MANUTENCAO")
        manutencoes = await cursor.fetchall()
        return {"manutencoes": [list(manut) for manut in manutencoes]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == '__main__':
    uvicorn.run("api:app", port=8080, host='0.0.0.0', reload=True, workers=1, proxy_headers=True)