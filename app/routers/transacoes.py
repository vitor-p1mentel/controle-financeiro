from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/transacoes", tags=["transações"])


def _garantir_categoria(db: Session, categoria_id: int) -> None:
    if db.get(models.Categoria, categoria_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")


def _buscar_ou_404(db: Session, transacao_id: int) -> models.Transacao:
    transacao = db.get(models.Transacao, transacao_id)
    if transacao is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Transação não encontrada")
    return transacao


@router.post("", response_model=schemas.TransacaoOut, status_code=status.HTTP_201_CREATED)
def criar(dados: schemas.TransacaoCreate, db: Session = Depends(get_db)):
    _garantir_categoria(db, dados.categoria_id)
    transacao = models.Transacao(**dados.model_dump())
    db.add(transacao)
    db.commit()
    db.refresh(transacao)
    return transacao


@router.get("", response_model=list[schemas.TransacaoOut])
def listar(
    mes: str | None = Query(default=None, pattern=r"^\d{4}-(0[1-9]|1[0-2])$"),
    tipo: models.TipoTransacao | None = None,
    categoria_id: int | None = None,
    limite: int = Query(default=50, ge=1, le=200),
    deslocamento: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    consulta = select(models.Transacao)

    if mes:
        ano, numero_mes = map(int, mes.split("-"))
        inicio = date(ano, numero_mes, 1)
        if numero_mes == 12:
            fim = date(ano + 1, 1, 1)
        else:
            fim = date(ano, numero_mes + 1, 1)
        consulta = consulta.where(
            models.Transacao.data >= inicio,
            models.Transacao.data < fim,
        )
    if tipo:
        consulta = consulta.where(models.Transacao.tipo == tipo)
    if categoria_id:
        consulta = consulta.where(models.Transacao.categoria_id == categoria_id)

    consulta = (
        consulta.order_by(models.Transacao.data.desc(), models.Transacao.id.desc())
        .limit(limite)
        .offset(deslocamento)
    )
    return db.scalars(consulta).all()


@router.get("/{transacao_id}", response_model=schemas.TransacaoOut)
def obter(transacao_id: int, db: Session = Depends(get_db)):
    return _buscar_ou_404(db, transacao_id)


@router.patch("/{transacao_id}", response_model=schemas.TransacaoOut)
def atualizar(
    transacao_id: int,
    dados: schemas.TransacaoUpdate,
    db: Session = Depends(get_db),
):
    transacao = _buscar_ou_404(db, transacao_id)
    mudancas = dados.model_dump(exclude_none=True)

    if "categoria_id" in mudancas:
        _garantir_categoria(db, mudancas["categoria_id"])

    for campo, valor in mudancas.items():
        setattr(transacao, campo, valor)

    db.commit()
    db.refresh(transacao)
    return transacao


@router.delete("/{transacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def apagar(transacao_id: int, db: Session = Depends(get_db)):
    transacao = _buscar_ou_404(db, transacao_id)
    db.delete(transacao)
    db.commit()