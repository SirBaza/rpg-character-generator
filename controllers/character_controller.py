from fastapi import APIRouter, HTTPException, Depends
from typing import List
from domain.models import Character, DiceRoll
from services.character_service import CharacterGeneratorService, DiceService
from repositories.character_repository import CharacterRepository

router = APIRouter()

# Dependências
def get_character_service():
    return CharacterGeneratorService()

def get_dice_service():
    return DiceService()

def get_character_repository():
    return CharacterRepository()

@router.get("/character/random", response_model=Character)
async def generate_random_character(
    service: CharacterGeneratorService = Depends(get_character_service)
):
    """Gera um personagem aleatório"""
    try:
        character = service.generate_random_character()
        return character
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar personagem: {str(e)}")

@router.post("/character", response_model=Character)
async def save_character(
    character: Character,
    repository: CharacterRepository = Depends(get_character_repository)
):
    """Salva um personagem no banco de dados"""
    try:
        saved_character = repository.save_character(character)
        return saved_character
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar personagem: {str(e)}")

@router.get("/character/{character_id}", response_model=Character)
async def get_character(
    character_id: int,
    repository: CharacterRepository = Depends(get_character_repository)
):
    """Busca um personagem pelo ID"""
    character = repository.get_character(character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    return character

@router.get("/characters", response_model=List[Character])
async def list_characters(
    limit: int = None,
    repository: CharacterRepository = Depends(get_character_repository)
):
    """Lista personagens salvos"""
    try:
        characters = repository.list_characters(limit)
        return characters
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar personagens: {str(e)}")

@router.delete("/character/{character_id}")
async def delete_character(
    character_id: int,
    repository: CharacterRepository = Depends(get_character_repository)
):
    """Remove um personagem"""
    success = repository.delete_character(character_id)
    if not success:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    return {"message": "Personagem removido com sucesso"}

@router.delete("/characters/clear")
async def clear_database(
    repository: CharacterRepository = Depends(get_character_repository)
):
    """Limpa todos os personagens do banco de dados"""
    try:
        count = repository.clear_all_characters()
        return {"message": f"Banco de dados limpo com sucesso. {count} personagens removidos."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao limpar banco de dados: {str(e)}")

@router.get("/roll/{dice}", response_model=DiceRoll)
async def roll_dice(
    dice: str,
    service: DiceService = Depends(get_dice_service)
):
    """Simula rolagem de dados (ex: 1d20+3, 3d6, 2d8-1)"""
    try:
        result = service.roll_dice(dice)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao rolar dados: {str(e)}")
