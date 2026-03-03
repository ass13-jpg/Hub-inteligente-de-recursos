import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Carregar .env da pasta backend
env_path = Path(__file__).parent.parent / ".env"
print(f"Carregando .env de: {env_path}")
load_dotenv(env_path)

print(f"GEMINI_API_KEY carregada: {bool(os.getenv('GEMINI_API_KEY'))}")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes import resources, ai, health

# Inicializar banco de dados
init_db()

# Configurar CORS
app = FastAPI(
    title="Hub Inteligente de Recursos Educacionais",
    description="API para catalogação inteligente de recursos educacionais",
    version="1.0.0"
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "[]")
if isinstance(allowed_origins, str):
    import json
    try:
        allowed_origins = json.loads(allowed_origins)
    except:
        allowed_origins = ["http://localhost:3000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(health.router)
app.include_router(resources.router)
app.include_router(ai.router)

@app.get("/")
def read_root():
    return {
        "message": "🎓 Hub Inteligente de Recursos Educacionais",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)