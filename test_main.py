import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "RPG Character Generator API" in response.json()["message"]

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_generate_random_character():
    response = client.get("/api/v1/character/random")
    assert response.status_code == 200
    
    character = response.json()
    assert "nome" in character
    assert "raca" in character
    assert "classe" in character
    assert "atributos" in character
    assert "pontos_vida" in character

def test_roll_dice():
    response = client.get("/api/v1/roll/1d20")
    assert response.status_code == 200
    
    result = response.json()
    assert "result" in result
    assert "rolls" in result
    assert 1 <= result["result"] <= 20

def test_roll_dice_with_modifier():
    response = client.get("/api/v1/roll/1d20+5")
    assert response.status_code == 200
    
    result = response.json()
    assert 6 <= result["result"] <= 25

def test_invalid_dice_notation():
    response = client.get("/api/v1/roll/invalid")
    assert response.status_code == 400
