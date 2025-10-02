import random
import re
from typing import List, Tuple
from domain.models import Character, CharacterClass, Race, Attributes, Equipment, DiceRoll

class CharacterGeneratorService:
    """Serviço responsável pela geração de personagens"""
    
    def __init__(self):
        self.pericias_por_classe = {
            CharacterClass.GUERREIRO: ["Atletismo", "Intimidação", "Sobrevivência", "Percepção"],
            CharacterClass.MAGO: ["Arcana", "História", "Investigação", "Medicina"],
            CharacterClass.LADRAO: ["Acrobacia", "Furtividade", "Prestidigitação", "Percepção"],
            CharacterClass.CLERIGO: ["História", "Medicina", "Persuasão", "Religião"],
            CharacterClass.PALADINO: ["Atletismo", "Intimidação", "Medicina", "Religião"],
            CharacterClass.RANGER: ["Sobrevivência", "Percepção", "Rastreamento", "Trato com Animais"]
        }
        
        self.equipamentos_por_classe = {
            CharacterClass.GUERREIRO: {"armas": ["Espada Longa", "Escudo"], "armadura": "Cota de Malha", "itens": ["Kit de Aventureiro"]},
            CharacterClass.MAGO: {"armas": ["Cajado"], "armadura": "Robes", "itens": ["Grimório", "Kit de Componentes"]},
            CharacterClass.LADRAO: {"armas": ["Punhal", "Arco Curto"], "armadura": "Armadura de Couro", "itens": ["Kit de Ladrão"]},
            CharacterClass.CLERIGO: {"armas": ["Martelo de Guerra", "Escudo"], "armadura": "Cota de Malha", "itens": ["Símbolo Sagrado"]},
            CharacterClass.PALADINO: {"armas": ["Espada Longa", "Escudo"], "armadura": "Cota de Placas", "itens": ["Símbolo Sagrado"]},
            CharacterClass.RANGER: {"armas": ["Arco Longo", "Espada Curta"], "armadura": "Armadura de Couro", "itens": ["Kit de Sobrevivência"]}
        }

    def generate_attributes(self) -> Attributes:
        """Gera atributos aleatórios usando 4d6, descartando o menor"""
        def roll_attribute():
            rolls = [random.randint(1, 6) for _ in range(4)]
            rolls.sort(reverse=True)
            return sum(rolls[:3])  # Soma os 3 maiores
        
        return Attributes(
            forca=roll_attribute(),
            destreza=roll_attribute(),
            constituicao=roll_attribute(),
            inteligencia=roll_attribute(),
            sabedoria=roll_attribute(),
            carisma=roll_attribute()
        )

    def calculate_hit_points(self, classe: CharacterClass, constituicao: int, nivel: int = 1) -> int:
        """Calcula pontos de vida baseado na classe e constituição"""
        hit_dice = {
            CharacterClass.GUERREIRO: 10,
            CharacterClass.PALADINO: 10,
            CharacterClass.RANGER: 10,
            CharacterClass.CLERIGO: 8,
            CharacterClass.LADRAO: 8,
            CharacterClass.MAGO: 6
        }
        
        base_hp = hit_dice[classe]
        con_modifier = (constituicao - 10) // 2
        return base_hp + con_modifier + ((nivel - 1) * (hit_dice[classe] // 2 + 1 + con_modifier))

    def generate_random_character(self) -> Character:
        """Gera um personagem completamente aleatório"""
        raca = random.choice(list(Race))
        classe = random.choice(list(CharacterClass))
        atributos = self.generate_attributes()
        
        # Aplicar bônus raciais
        atributos = self._apply_racial_bonuses(atributos, raca)
        
        pontos_vida = self.calculate_hit_points(classe, atributos.constituicao)
        
        # Equipamentos baseados na classe
        equipamentos_base = self.equipamentos_por_classe[classe]
        equipamentos = Equipment(
            armas=equipamentos_base["armas"],
            armadura=equipamentos_base["armadura"],
            itens=equipamentos_base["itens"],
            dinheiro=random.randint(50, 200)
        )
        
        # Perícias baseadas na classe
        pericias_disponiveis = self.pericias_por_classe[classe]
        pericias = random.sample(pericias_disponiveis, min(2, len(pericias_disponiveis)))
        
        nomes = ["Aeren", "Berris", "Cithreth", "Drannor", "Enna", "Galinndan", "Halimath", "Immeral", "Ivellios", "Korfel"]
        nome = random.choice(nomes)
        
        return Character(
            nome=nome,
            raca=raca,
            classe=classe,
            atributos=atributos,
            pontos_vida=pontos_vida,
            equipamentos=equipamentos,
            pericias=pericias
        )

    def _apply_racial_bonuses(self, atributos: Attributes, raca: Race) -> Attributes:
        """Aplica bônus raciais aos atributos"""
        bonuses = {
            Race.HUMANO: {"forca": 1, "destreza": 1, "constituicao": 1, "inteligencia": 1, "sabedoria": 1, "carisma": 1},
            Race.ELFO: {"destreza": 2, "inteligencia": 1},
            Race.ANAO: {"constituicao": 2, "sabedoria": 1},
            Race.HALFLING: {"destreza": 2, "carisma": 1},
            Race.MEIO_ELFO: {"carisma": 2, "forca": 1},
            Race.ORC: {"forca": 2, "constituicao": 1}
        }
        
        if raca in bonuses:
            bonus = bonuses[raca]
            atributos.forca += bonus.get("forca", 0)
            atributos.destreza += bonus.get("destreza", 0)
            atributos.constituicao += bonus.get("constituicao", 0)
            atributos.inteligencia += bonus.get("inteligencia", 0)
            atributos.sabedoria += bonus.get("sabedoria", 0)
            atributos.carisma += bonus.get("carisma", 0)
        
        return atributos

class DiceService:
    """Serviço para simulação de rolagem de dados"""
    
    def roll_dice(self, dice_notation: str) -> DiceRoll:
        """
        Rola dados baseado na notação padrão (ex: 1d20+3, 3d6, 2d8-1)
        """
        # Parse da notação de dados
        pattern = r'(\d+)d(\d+)([+-]\d+)?'
        match = re.match(pattern, dice_notation.replace(' ', ''))
        
        if not match:
            raise ValueError(f"Notação de dado inválida: {dice_notation}")
        
        num_dice = int(match.group(1))
        die_size = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0
        
        if num_dice < 1 or num_dice > 100:
            raise ValueError("Número de dados deve estar entre 1 e 100")
        
        if die_size < 2 or die_size > 100:
            raise ValueError("Tamanho do dado deve estar entre 2 e 100")
        
        # Rolar os dados
        rolls = [random.randint(1, die_size) for _ in range(num_dice)]
        total = sum(rolls) + modifier
        
        return DiceRoll(
            dice_notation=dice_notation,
            result=total,
            rolls=rolls,
            modifier=modifier
        )
