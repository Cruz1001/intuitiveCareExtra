from fastapi import FastAPI, Query, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware
import os

# Configuração do FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# Configuração do Banco de Dados
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://usuario:senha@host:porta/nome_do_banco")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo do Banco de Dados
class OperadoraDB(Base):
    __tablename__ = "operadoras"
    Registro_ANS = Column(String, primary_key=True)
    CNPJ = Column(String)
    Razao_Social = Column(String)
    Nome_Fantasia = Column(String)
    Modalidade = Column(String)
    Logradouro = Column(String)
    Numero = Column(String)
    Complemento = Column(String)
    Bairro = Column(String)
    Cidade = Column(String)
    UF = Column(String)
    CEP = Column(String)
    DDD = Column(String)
    Telefone = Column(String)
    Fax = Column(String)
    Endereco_eletronico = Column(String)
    Representante = Column(String)
    Cargo_Representante = Column(String)
    Regiao_de_Comercializacao = Column(String)
    Data_Registro_ANS = Column(String)

Base.metadata.create_all(bind=engine)


class Operadora(BaseModel):
    Registro_ANS: str
    CNPJ: str
    Razao_Social: str
    Nome_Fantasia: str
    Modalidade: str
    Logradouro: str
    Numero: str
    Complemento: str
    Bairro: str
    Cidade: str
    UF: str
    CEP: str
    DDD: str
    Telefone: str
    Fax: str
    Endereco_eletronico: str
    Representante: str
    Cargo_Representante: str
    Regiao_de_Comercializacao: str
    Data_Registro_ANS: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para buscar operadoras
@app.get("/buscar-operadoras", response_model=List[Operadora])
async def buscar_operadoras(query: str = Query("", min_length=0), db: Session = Depends(get_db)):
    """Retorna uma lista de operadoras filtradas pelo Nome Fantasia."""
    if query:
        operadoras = db.query(OperadoraDB).filter(OperadoraDB.Nome_Fantasia.ilike(f"%{query}%")).all()
    else:
        operadoras = db.query(OperadoraDB).all()
    return [Operadora(**op.__dict__) for op in operadoras]
