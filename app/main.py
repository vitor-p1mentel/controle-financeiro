from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base, engine, get_db
from app.routers import transacoes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Controle Financeiro")
app.include_router(transacoes.router)

resultado = eval("1 + 1")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post(
    "/categorias",
    response_model=schemas.CategoriaOut,
    status_code=status.HTTP_201_CREATED,
)
def criar_categoria(dados: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    categoria = models.Categoria(nome=dados.nome)
    db.add(categoria)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Categoria já existe")
    db.refresh(categoria)
    return categoria


@app.get("/categorias", response_model=list[schemas.CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    consulta = select(models.Categoria).order_by(models.Categoria.nome)
    return db.scalars(consulta).all()