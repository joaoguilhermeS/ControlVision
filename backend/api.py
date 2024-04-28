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
from cryptography.fernet import Fernet
import jwt
from typing import List, Optional
from pydantic import BaseModel
import math
from fastapi.responses import StreamingResponse
from openai import OpenAI
import requests
import json


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
        title="API - Riskeen",
        version="0.1",
        description="Página de API do projeto GPT Riskeen.",
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

async def create_user(email: str, username: str, password: str, team_size: int, plan: str, tokens_available: int, company_name: str, name: str):
    fernet_key = b'aqkh5XBvqDk_lrN1XaH2UBsA2pC73v265SYZERcEeJs='
    fernet = Fernet(fernet_key)
    encrypted_password = fernet.encrypt(password.encode()).decode()
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=os.getenv("DB_HOST"), port=3306, user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), db = os.getenv("DB_DATABASE"))
        cursor = await conn.cursor()
        # Check if the email already exists in the database
        await cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        existing_email = await cursor.fetchone()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered.")

        await cursor.execute("INSERT INTO users (email, username, password, team_size, plan, tokens_available, company_name, name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                             (email, username, encrypted_password, team_size, plan, tokens_available, company_name, name))
        await conn.commit()
    except Exception as e:  
        # Consider using a logging framework for logging before raising exceptions
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=f"An error occurred while creating the user: {e}.")

async def update_user(email: str, username: str, password: str, team_size: int, plan: str, tokens_available: int, company_name: str, name: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()

        await cursor.execute("UPDATE users SET username=%s, password=%s, team_size=%s, plan=%s, tokens_available=%s, company_name=%s, name=%s, updated_at=CURRENT_TIMESTAMP WHERE email=%s",
                             (username, password, team_size, plan, tokens_available, company_name, name, email))
        await conn.commit()
    except Exception as e:
        print(f"\n\n\nError: {e}\n\n\n")
    # finally:
    #     if cursor:
    #         try:
    #             await cursor.close()
    #         except Exception as e:
    #             print(f"\n\n\n2Error2: {e}\n\n\n")
    #     if conn:
    #         try: 
    #             await conn.close()
    #         except Exception as e:
    #             print(f"\n\n\n3Error3: {e}\n\n\n")

async def delete_user(email: str, name: str):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        # First, delete all projects related to the user
        await cursor.execute("DELETE FROM projects WHERE user_id IN (SELECT user_id FROM users WHERE email = %s)", (email,))
        await conn.commit()
        # Now, delete the user
        await cursor.execute("DELETE FROM users WHERE email = %s", (email,))
        affected_rows = cursor.rowcount
        await conn.commit()
        if affected_rows == 0:
            raise HTTPException(status_code=404, detail="User not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def create_project(project_name: str, client_name: str, manager_name: str, date_created: str, revision_responsible_name: str, date_last_review: str, base_project_price: float, management_system: str, process_risks_identification: str, monitoring_responsible_people: str, project_context: str, user_id: int):
    conn = None
    cursor = None
    date_created_str = '2024-03-31T00:24:24Z'
    date_created_obj = datetime.fromisoformat(date_created_str.rstrip('Z'))
    formatted_date_created = date_created_obj.strftime('%Y-%m-%d %H:%M:%S')
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        # Insert the new project into the database

        if(date_last_review is not None):
            date_last_review = date_created

        try:
            if(len(date_last_review) > 1):
                pass
        except:
            date_last_review = date_created

        await cursor.execute(
            "INSERT INTO projects (project_name, client_name, manager_name, date_created, revision_responsible_name, date_last_review, base_project_price, management_system, process_risks_identification, monitoring_responsible_people, project_context, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (project_name, client_name, manager_name, date_created, revision_responsible_name, date_last_review, base_project_price, management_system, process_risks_identification, monitoring_responsible_people, project_context, user_id)
        )
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/register-user")
async def register_user(
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    team_size: int = Form(...),
    plan: str = Form(...),
    tokens_available: int = Form(...),
    company_name: str = Form(...),
    name: str = Form(...)
):
    try:
        await create_user(email, username, password, team_size, plan, tokens_available, company_name, name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"message": "User registered successfully!"}

@app.put("/update-user/{email}")
async def update_user_endpoint(
    email: str,
    username: str = Form(...),
    password: str = Form(...),
    team_size: int = Form(...),
    plan: str = Form(...),
    tokens_available: int = Form(...),
    company_name: str = Form(...),
    name: str = Form(...)
):
    try:
        await update_user(email, username, password, team_size, plan, tokens_available, company_name, name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"message": "User updated successfully!"}

@app.delete("/delete-user/{email}")
async def delete_user_endpoint(email: str):
    """Delete a user by email."""
    try:
        success = await delete_user(email)
        if not success:
            raise HTTPException(status_code=404, detail="User not found.")
        return {"message": "User deleted successfully!"}
    except Exception as e:
        if "object NoneType can't be used in 'await' expression" in str(e):
            return {"message": "User deleted successfully!"}
        raise HTTPException(status_code=400, detail=str(e))

async def get_user(user_id: int):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = await cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        fernet_key = b'aqkh5XBvqDk_lrN1XaH2UBsA2pC73v265SYZERcEeJs='
        fernet = Fernet(fernet_key)
        decrypted_password_bytes = fernet.decrypt(user[3].encode())
        decrypted_password = decrypted_password_bytes.decode()
        # print(decrypted_password)

        user_data = {
            "user_id": user[0],
            "email": user[1],
            "username": user[2],
            "password": decrypted_password,
            "created_at": user[4],
            "updated_at": user[5],
            "team_size": user[6],
            "plan": user[7],
            "tokens_available": user[8],
            "company_name": user[9]
        }
        return user_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get-users/{user_id}")
async def get_user_endpoint(user_id: int):
    return await get_user(user_id)

@app.post("/create-usuario")
async def create_usuario(nome: str = Form(...), senha: str = Form(...), usuario: str = Form(...), cpf: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("INSERT INTO USUARIO (nome, senha, usuario, cpf) VALUES (%s, %s, %s, %s)", (nome, senha, usuario, cpf))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            await cursor.close()
        if conn:
            await conn.close()
    return {"message": "Usuario created successfully!"}

@app.put("/update-usuario/{matricula}")
async def update_usuario(matricula: int, nome: str = Form(...), senha: str = Form(...), usuario: str = Form(...), cpf: int = Form(...)):
    conn = None
    cursor = None
    try:
        conn = await aiomysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_database)
        cursor = await conn.cursor()
        await cursor.execute("UPDATE USUARIO SET nome=%s, senha=%s, usuario=%s, cpf=%s WHERE matricula=%s", (nome, senha, usuario, cpf, matricula))
        await conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            await cursor.close()
        if conn:
            await conn.close()
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
    finally:
        if cursor:
            await cursor.close()
        if conn:
            await conn.close()
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
    finally:
        if cursor:
            await cursor.close()
        if conn:
            await conn.close()
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
    finally:
        if cursor:
            await cursor.close()
        if conn:
            await conn.close()
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
    finally:
        if cursor:
            await cursor.close()
        if conn:
            await conn.close()
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
    finally:
        if cursor:
            await cursor.close()
        if conn:
            await conn.close()
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
    finally:
        if cursor:
            await cursor.close()
        if conn:
            await conn.close()
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
    finally:
        if cursor:
            await cursor.close()
        if conn:
            await conn.close()
    return {"message": "Observacoes deleted successfully!"}

if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, host='0.0.0.0', reload=True, workers=1, proxy_headers=True)
