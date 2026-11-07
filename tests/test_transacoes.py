def criar_categoria(client, nome="Mercado"):
    return client.post("/categorias", json={"nome": nome}).json()["id"]


def nova_transacao(categoria_id, **extra):
    base = {
        "tipo": "saida",
        "valor_centavos": 1250,
        "descricao": "Pão e leite",
        "data": "2026-11-05",
        "categoria_id": categoria_id,
    }
    return {**base, **extra}


def test_criar_transacao(client):
    cat = criar_categoria(client)
    r = client.post("/transacoes", json=nova_transacao(cat))
    assert r.status_code == 201
    assert r.json()["valor_centavos"] == 1250
    assert r.json()["tipo"] == "saida"


def test_categoria_inexistente(client):
    r = client.post("/transacoes", json=nova_transacao(999))
    assert r.status_code == 404


def test_valor_zero_ou_negativo_e_rejeitado(client):
    cat = criar_categoria(client)
    for valor in (0, -100):
        r = client.post("/transacoes", json=nova_transacao(cat, valor_centavos=valor))
        assert r.status_code == 422


def test_tipo_invalido_e_rejeitado(client):
    cat = criar_categoria(client)
    r = client.post("/transacoes", json=nova_transacao(cat, tipo="roubo"))
    assert r.status_code == 422


def test_listar_filtrando_por_mes_e_tipo(client):
    cat = criar_categoria(client)
    client.post("/transacoes", json=nova_transacao(cat, data="2026-11-05"))
    client.post("/transacoes", json=nova_transacao(cat, data="2026-10-30"))
    client.post("/transacoes", json=nova_transacao(cat, tipo="entrada", data="2026-11-01"))

    r = client.get("/transacoes", params={"mes": "2026-11"})
    assert len(r.json()) == 2

    r = client.get("/transacoes", params={"mes": "2026-11", "tipo": "saida"})
    assert len(r.json()) == 1


def test_mes_com_formato_invalido(client):
    r = client.get("/transacoes", params={"mes": "novembro"})
    assert r.status_code == 422


def test_atualizar_apenas_o_valor(client):
    cat = criar_categoria(client)
    transacao_id = client.post("/transacoes", json=nova_transacao(cat)).json()["id"]
    r = client.patch(f"/transacoes/{transacao_id}", json={"valor_centavos": 2000})
    assert r.status_code == 200
    assert r.json()["valor_centavos"] == 2000
    assert r.json()["descricao"] == "Pão e leite"


def test_nao_e_possivel_alterar_o_id(client):
    cat = criar_categoria(client)
    transacao_id = client.post("/transacoes", json=nova_transacao(cat)).json()["id"]
    r = client.patch(f"/transacoes/{transacao_id}", json={"id": 999, "valor_centavos": 100})
    assert r.json()["id"] == transacao_id


def test_apagar_transacao(client):
    cat = criar_categoria(client)
    transacao_id = client.post("/transacoes", json=nova_transacao(cat)).json()["id"]
    assert client.delete(f"/transacoes/{transacao_id}").status_code == 204
    assert client.get(f"/transacoes/{transacao_id}").status_code == 404