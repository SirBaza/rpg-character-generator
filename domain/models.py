from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class CharacterClass(str, Enum):
    GUERREIRO = "Guerreiro"
    MAGO = "Mago"
    LADRAO = "Ladrão"
    CLERIGO = "Clérigo"
    PALADINO = "Paladino"
    RANGER = "Ranger"

class Race(str, Enum):
    HUMANO = "Humano"
    ELFO = "Elfo"
    ANAO = "Anão"
    HALFLING = "Halfling"
    MEIO_ELFO = "Meio-Elfo"
    ORC = "Orc"

class Attributes(BaseModel):
    forca: int
    destreza: int
    constituicao: int
    inteligencia: int
    sabedoria: int
    carisma: int
    
    def get_modifier(self, attribute_value: int) -> int:
        """Calcula o modificador de um atributo"""
        return (attribute_value - 10) // 2

class Equipment(BaseModel):
    armas: List[str]
    armadura: str
    itens: List[str]
    dinheiro: int

class Character(BaseModel):
    id: Optional[int] = None
    nome: str
    raca: Race
    classe: CharacterClass
    nivel: int = 1
    atributos: Attributes
    pontos_vida: int
    equipamentos: Equipment
    pericias: List[str]
    
    class Config:
        from_attributes = True

class DiceRoll(BaseModel):
    dice_notation: str
    result: int
    rolls: List[int]
    modifier: int = 0
