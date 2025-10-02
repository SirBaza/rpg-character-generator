from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from controllers.character_controller import router as character_router
import os

app = FastAPI(
    title="RPG Character Generator",
    description="Microsserviço para geração automática de fichas de personagens de RPG",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir rotas da API
app.include_router(character_router, prefix="/api/v1", tags=["characters"])

@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serve a página principal"""
    with open("static/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/api")
async def api_info():
    return {
        "message": "RPG Character Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "generate_random_character": "/api/v1/character/random",
            "save_character": "/api/v1/character",
            "get_character": "/api/v1/character/{id}",
            "list_characters": "/api/v1/characters",
            "roll_dice": "/api/v1/roll/{dice}"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "RPG Character Generator is running!"}

if __name__ == "__main__":
    import uvicorn
    print("🎲 Iniciando RPG Character Generator...")
    print("📱 Interface Web: http://localhost:8000")
    print("📚 Documentação da API: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
