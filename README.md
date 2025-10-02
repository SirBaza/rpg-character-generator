# RPG Character Generator

Um microsserviço para geração automática de fichas de personagens de RPG.

## Funcionalidades

- Geração automática de personagens
- Simulação de rolagem de dados
- Armazenamento de fichas
- API REST com documentação automática

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
uvicorn main:app --reload
```

## Endpoints

- `GET /character/random` - Gera um personagem aleatório
- `GET /roll/{dice}` - Simula rolagem de dados (ex: 1d20+3)
- `GET /character/{id}` - Retorna personagem salvo
- `POST /character` - Salva um novo personagem

## Docker

```bash
docker build -t rpg-character-generator .
docker run -p 8000:8000 rpg-character-generator
```
