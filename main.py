from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.character_controller import router as character_router

app = FastAPI(
    title="RPG Character Generator API",
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

# Incluir rotas
app.include_router(character_router, prefix="/api/v1", tags=["characters"])

@app.get("/")
async def root():
    return {
        "message": "RPG Character Generator API",
        "version": "1.0.0",
        "docs": "/docs",
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
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
