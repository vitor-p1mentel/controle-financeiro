from fastapi import FastAPI

app = FastAPI(title="Controle Financeiro")

@app.get("/health")
def health():
    return {"status": "ok"}