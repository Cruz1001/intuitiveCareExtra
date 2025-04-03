from fastapi import FastAPI, Query, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware
import os
import csv
from fastapi.staticfiles import StaticFiles

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://intuitivedb_user:gU2YjyStnGMOwbZkaroPW1WZxETqgMio@dpg-cvnd5jripnbc73aungg0-a.oregon-postgres.render.com/intuitivedb"
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class OperadoraDB(Base):
    __tablename__ = "operadoras"
    
    Registro_ANS = Column(String, primary_key=True)
    CNPJ = Column(String, nullable=True)
    Razao_Social = Column(String, nullable=True)
    Nome_Fantasia = Column(String, nullable=True)
    Modalidade = Column(String, nullable=True)
    Logradouro = Column(String, nullable=True)
    Numero = Column(String, nullable=True)
    Complemento = Column(String, nullable=True)
    Bairro = Column(String, nullable=True)
    Cidade = Column(String, nullable=True)
    UF = Column(String, nullable=True)
    CEP = Column(String, nullable=True)
    DDD = Column(String, nullable=True)
    Telefone = Column(String, nullable=True)
    Fax = Column(String, nullable=True)
    Endereco_eletronico = Column(String, nullable=True)
    Representante = Column(String, nullable=True)
    Cargo_Representante = Column(String, nullable=True)
    Regiao_de_Comercializacao = Column(String, nullable=True)
    Data_Registro_ANS = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)


class Operadora(BaseModel):
    Registro_ANS: str
    CNPJ: str | None = None
    Razao_Social: str | None = None
    Nome_Fantasia: str | None = None
    Modalidade: str | None = None
    Logradouro: str | None = None
    Numero: str | None = None
    Complemento: str | None = None
    Bairro: str | None = None
    Cidade: str | None = None
    UF: str | None = None
    CEP: str | None = None
    DDD: str | None = None
    Telefone: str | None = None
    Fax: str | None = None
    Endereco_eletronico: str | None = None
    Representante: str | None = None
    Cargo_Representante: str | None = None
    Regiao_de_Comercializacao: str | None = None
    Data_Registro_ANS: str | None = None


def get_db():
    db = SessionLocal()
    print("📡 Conectando ao banco de dados...")
    try:
        yield db
    finally:
        db.close()

@app.get("/buscar-operadoras", response_model=List[Operadora])
async def buscar_operadoras(
    query: str = Query("", min_length=0), db: Session = Depends(get_db)
):
    print(" Endpoint /buscar-operadoras foi chamado!")  # Log para testar
    operadoras = db.query(OperadoraDB).filter(OperadoraDB.Nome_Fantasia.ilike(f"%{query}%")).all() if query else db.query(OperadoraDB).all()
    
    print(f" Encontradas {len(operadoras)} operadoras.")  # Log para testar o banco
    
    return [Operadora(**op.__dict__) for op in operadoras]


def importar_csv():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "arquivos", "Relatorio_cadop.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError("Arquivo CSV não encontrado.")
    
    db = SessionLocal()
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")  
            next(reader, None)

            for row in reader:
                if not row or all(cell.strip() == "" for cell in row): 
                    continue
                
                while len(row) < 20:
                    row.append(None)
                
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


@app.post("/importar-csv")
async def importar_operadoras():
    try:
        importar_csv()
        return {"message": "CSV importado com sucesso!"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

static_path = os.path.join(os.path.dirname(__file__), "dist")
if os.path.exists(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")
else:
    print(" A pasta 'dist' não foi encontrada! Não será possível servir o frontend.")
