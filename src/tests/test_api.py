import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app, business_agent

client = TestClient(app)

def override_verify_api_key():
    return None

app.dependency_overrides = {}
app.dependency_overrides[getattr(__import__('src.auth', fromlist=['verify_api_key']), 'verify_api_key')] = override_verify_api_key

@patch('src.agent.BusinessAgent.answer')
@patch('src.followup.FollowUpAgent.suggest')
def test_query_business(mock_suggest, mock_answer):
    mock_answer.return_value = ("Here are vegan cafes in Bondi...", [
        {"name": "Vegan Cafe Bondi", "category": "Cafe", "location": "Bondi", "description": "A vegan cafe in Bondi."},
        {"name": "Green Eats", "category": "Restaurant", "location": "Bondi", "description": "Healthy vegan food."},
        {"name": "Plant Power", "category": "Diner", "location": "Bondi", "description": "Vegan burgers and shakes."}
    ])
    mock_suggest.return_value = "Would you like to see vegan restaurants in another suburb?"
    response = client.post("/query?session_id=test123", json={"query": "Find vegan cafes near Bondi"}, headers={"x-api-key": "test"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "top_results" in data
    assert len(data["top_results"]) == 3
    assert any("vegan" in b["description"].lower() for b in data["top_results"])
    assert "followup" in data

@patch('src.main.business_agent.retriever.load_and_embed', return_value=None)
def test_upload_data(mock_load_and_embed):
    test_json = [
        {"name": "Test Biz", "category": "Cafe", "location": "Test", "description": "Test desc"}
    ]
    import io
    file = io.BytesIO(bytes(str(test_json).replace("'", '"'), 'utf-8'))
    file.name = 'test.json'
    response = client.post("/upload", files={"file": (file.name, file, "application/json")}, headers={"x-api-key": "test"})
    assert response.status_code == 200
    assert "Uploaded and embedded" in response.json()["message"]
