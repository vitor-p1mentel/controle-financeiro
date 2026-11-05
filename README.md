# Controle Financeiro

Aplicação web para registrar entradas e saídas de dinheiro, ver gráficos
do mês e gerar relatórios com dicas de economia.

## Stack
Python, FastAPI, SQLite, HTML/CSS/JS, Docker, GitHub Actions

## Como rodar
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

## Testes
python -m pytest
