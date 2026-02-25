from fastapi import FastAPI

app = FastAPI(title="PDF Hub")

@app.get("/health")
def health():
    return {"status": "ok"}