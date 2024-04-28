from fastapi import FastAPI, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from schemas import UsuarioSchema

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/usuarios/", response_model=UsuarioSchema)
def create_usuario_endpoint(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    return create_usuario(db, usuario)

@app.get("/usuarios/{matricula}", response_model=UsuarioSchema)
def read_usuario(matricula: int, db: Session = Depends(get_db)):
    db_usuario = get_usuario(db, matricula)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return db_usuario

@app.delete("/usuarios/{matricula}")
def delete_usuario_endpoint(matricula: int, db: Session = Depends(get_db)):
    result = delete_usuario(db, matricula)
    if result:
        return {"detail": "Usuario deleted"}
    else:
        raise HTTPException(status_code=404, detail="Usuario not found")

@app.put("/usuarios/{matricula}", response_model=UsuarioSchema)
def update_usuario_endpoint(matricula: int, usuario: UsuarioSchema, db: Session = Depends(get_db)):
    return update_usuario(db, matricula, usuario)
