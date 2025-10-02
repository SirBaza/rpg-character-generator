from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
from typing import List, Optional
from domain.models import Character

Base = declarative_base()

class CharacterEntity(Base):
    __tablename__ = "characters"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    raca = Column(String(50), nullable=False)
    classe = Column(String(50), nullable=False)
    nivel = Column(Integer, default=1)
    data_json = Column(Text, nullable=False)  # Armazenar todo o objeto como JSON

class CharacterRepository:
    def __init__(self, database_url: str = "sqlite:///./rpg_characters.db"):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(bind=self.engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = SessionLocal()

    def save_character(self, character: Character) -> Character:
        """Salva um personagem no banco de dados"""
        character_data = character.model_dump()
        character_json = json.dumps(character_data, ensure_ascii=False)
        
        entity = CharacterEntity(
            nome=character.nome,
            raca=character.raca.value,
            classe=character.classe.value,
            nivel=character.nivel,
            data_json=character_json
        )
        
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        
        # Atualizar o ID do character
        character.id = entity.id
        return character

    def get_character(self, character_id: int) -> Optional[Character]:
        """Busca um personagem pelo ID"""
        entity = self.db.query(CharacterEntity).filter(CharacterEntity.id == character_id).first()
        
        if entity:
            character_data = json.loads(entity.data_json)
            # Garantir que o ID seja definido corretamente
            character_data['id'] = entity.id
            return Character(**character_data)
        
        return None

    def list_characters(self, limit: int = None) -> List[Character]:
        """Lista personagens salvos"""
        query = self.db.query(CharacterEntity)
        if limit:
            query = query.limit(limit)
        entities = query.all()
        characters = []
        
        for entity in entities:
            character_data = json.loads(entity.data_json)
            # Garantir que o ID seja definido corretamente
            character_data['id'] = entity.id
            characters.append(Character(**character_data))
        
        return characters

    def delete_character(self, character_id: int) -> bool:
        """Remove um personagem do banco"""
        entity = self.db.query(CharacterEntity).filter(CharacterEntity.id == character_id).first()
        
        if entity:
            self.db.delete(entity)
            self.db.commit()
            return True
        
        return False

    def clear_all_characters(self) -> int:
        """Remove todos os personagens do banco de dados"""
        count = self.db.query(CharacterEntity).count()
        self.db.query(CharacterEntity).delete()
        self.db.commit()
        return count
