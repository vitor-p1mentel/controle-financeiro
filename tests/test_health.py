from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health():
    resposta = client.get("/health")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}

def test_criar_categoria(client):
    r = client.post("/categorias", json={"nome": "Mercado"})
    assert r.status_code == 201
    assert r.json()["nome"] == "Mercado"


def test_categoria_duplicada(client):
    client.post("/categorias", json={"nome": "Mercado"})
    r = client.post("/categorias", json={"nome": "Mercado"})
    assert r.status_code == 409


def test_nome_vazio_e_rejeitado(client):
    r = client.post("/categorias", json={"nome": ""})
    assert r.status_code == 422


def test_listar_categorias_em_ordem(client):
    client.post("/categorias", json={"nome": "Transporte"})
    client.post("/categorias", json={"nome": "Mercado"})
    r = client.get("/categorias")
    assert [c["nome"] for c in r.json()] == ["Mercado", "Transporte"]