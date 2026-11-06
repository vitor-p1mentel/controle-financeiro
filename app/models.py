import enum
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TipoTransacao(str, enum.Enum):
    ENTRADA = "entrada"
    SAIDA = "saida"


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True)

    transacoes: Mapped[list["Transacao"]] = relationship(back_populates="categoria")


class Transacao(Base):
    __tablename__ = "transacoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[TipoTransacao] = mapped_column(Enum(TipoTransacao))
    valor_centavos: Mapped[int]
    descricao: Mapped[str] = mapped_column(String(200))
    data: Mapped[date] = mapped_column(Date, default=date.today)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))

    categoria: Mapped["Categoria"] = relationship(back_populates="transacoes")