from fastapi import FastAPI, Query, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware
import os
import csv
from fastapi.staticfiles import StaticFiles

app = FastAPI()

static_path = os.path.join(os.path.dirname(__file__), "dist")
app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://intuitivedb_user:gU2YjyStnGMOwbZkaroPW1WZxETqgMio@dpg-cvnd5jripnbc73aungg0-a.oregon-postgres.render.com/intuitivedb")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


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


@app.get("/buscar-operadoras", response_model=List[Operadora])
async def buscar_operadoras(query: str = Query("", min_length=0), db: Session = Depends(get_db)):
    if query:
        operadoras = db.query(OperadoraDB).filter(OperadoraDB.Nome_Fantasia.ilike(f"%{query}%")).all()
    else:
        operadoras = db.query(OperadoraDB).all()
    return [Operadora(**op.__dict__) for op in operadoras]


def importar_csv():
    csv_path = os.path.join(os.path.dirname(__file__), "arquivos", "Relatorio_cadop.csv")

    if not os.path.exists(csv_path):
        raise FileNotFoundError("Arquivo CSV não encontrado na pasta 'arquivos'.")

    db = SessionLocal()
    
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # Pular cabeçalho

            for row in reader:
                operadora = OperadoraDB(
                    Registro_ANS=row[0], CNPJ=row[1], Razao_Social=row[2],
                    Nome_Fantasia=row[3], Modalidade=row[4], Logradouro=row[5],
                    Numero=row[6], Complemento=row[7], Bairro=row[8], Cidade=row[9],
                    UF=row[10], CEP=row[11], DDD=row[12], Telefone=row[13],
                    Fax=row[14], Endereco_eletronico=row[15], Representante=row[16],
                    Cargo_Representante=row[17], Regiao_de_Comercializacao=row[18],
                    Data_Registro_ANS=row[19]
                )
                db.add(operadora)

        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Rota para importar CSV
@app.post("/importar-csv")
async def importar_operadoras():
    try:
        importar_csv()
        return {"message": "CSV importado com sucesso!"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
