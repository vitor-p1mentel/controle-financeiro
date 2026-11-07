from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.models import TipoTransacao


class CategoriaCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=50)


class CategoriaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str

class TransacaoCreate(BaseModel):
    tipo: TipoTransacao
    valor_centavos: int = Field(gt=0, le=100_000_000)
    descricao: str = Field(min_length=1, max_length=200)
    data: date = Field(default_factory=date.today)
    categoria_id: int


class TransacaoUpdate(BaseModel):
    tipo: TipoTransacao | None = None
    valor_centavos: int | None = Field(default=None, gt=0, le=100_000_000)
    descricao: str | None = Field(default=None, min_length=1, max_length=200)
    data: date | None = None
    categoria_id: int | None = None


class TransacaoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo: TipoTransacao
    valor_centavos: int
    descricao: str
    data: date
    categoria_id: int