import bcrypt
from fastapi import FastAPI, Form, HTTPException
from pydantic import EmailStr
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, declarative_base
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configura la conexión (cambia usuario, contraseña, base_datos)
DATABASE_URL = "mysql+pymysql://talleruser:tallerpass123!@localhost:3306/taller2_db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define modelo usuario
class Usuario(Base):
    __tablename__ = "usuarios"
    email = Column(String(100), primary_key=True, index=True)
    password = Column(String(100))

Base.metadata.create_all(bind=engine)

def validar_contraseña(password: str) -> bool:
    if (len(password) < 8 or
        not re.search(r'[A-Z]', password) or
        not re.search(r'[a-z]', password) or
        not re.search(r'[0-9]', password) or
        not re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):
        return False
    return True

"""
@app.post("/register")
def register(email: EmailStr = Form(...), password: str = Form(...)):
    if not validar_contraseña(password):
        raise HTTPException(status_code=400, detail="La contraseña no cumple las reglas de seguridad")

    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        db.close()
        raise HTTPException(status_code=400, detail="Usuario ya registrado")

    nuevo_usuario = Usuario(email=email, password=password)
    db.add(nuevo_usuario)
    db.commit()
    db.close()
    return {"message": f"Usuario registrado: {email}"}
"""


@app.post("/register")
def register(email: EmailStr = Form(...), password: str = Form(...)):
    if not validar_contraseña(password):
        raise HTTPException(status_code=400, detail="La contraseña no cumple las reglas de seguridad")

    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        db.close()
        raise HTTPException(status_code=400, detail="Usuario ya registrado")

    # Hashea la contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    nuevo_usuario = Usuario(email=email, password=hashed_password.decode('utf-8'))
    db.add(nuevo_usuario)
    db.commit()
    db.close()
    return {"message": f"Usuario registrado: {email}"}


"""
@app.post("/login")
def login(email: EmailStr = Form(...), password: str = Form(...)):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    db.close()

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario no registrado")
    if usuario.password != password:
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    return {"message": "Inicio de sesión exitoso"}
"""


@app.post("/login")
def login(email: EmailStr = Form(...), password: str = Form(...)):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    db.close()

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario no registrado")

    # Verifica el hash
    if not bcrypt.checkpw(password.encode('utf-8'), usuario.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    return {"message": "Inicio de sesión exitoso"}

