from fastapi import FastAPI
from app.api.webhook_router import router as webhook_router
from app.db.database import init_db

app = FastAPI(title="Amigo de Patas WhatsApp Bot")

# Garante a criação do SQLite no inicio
init_db()

app.include_router(webhook_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Amigo de Patas Bot está rodando! 🐾"}

if __name__ == "__main__":
    import uvicorn
    # Setup mínimo pra demonstraçao portfolio local
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
