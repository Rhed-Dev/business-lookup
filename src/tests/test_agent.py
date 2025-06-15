import os
os.environ["OPENAI_API_TYPE"] = "openai"
import pytest
from unittest.mock import patch, MagicMock
from src.agent import BusinessAgent

@patch('openai.chat.completions.create')
@patch('src.agent.BusinessRetriever')
def test_agent_openai(mock_retriever, mock_openai_create):
    # Mock retriever returns fake businesses
    mock_retriever.return_value.search.return_value = [
        {"name": "Vegan Cafe Bondi", "category": "Cafe", "location": "Bondi", "description": "A vegan cafe in Bondi."},
        {"name": "Green Eats", "category": "Restaurant", "location": "Bondi", "description": "Healthy vegan food."},
        {"name": "Plant Power", "category": "Diner", "location": "Bondi", "description": "Vegan burgers and shakes."}
    ]
    # Mock OpenAI response
    mock_openai_create.return_value.choices = [MagicMock(message=MagicMock(content="Here are vegan cafes in Bondi..."))]
    agent = BusinessAgent()
    response, top_results = agent.answer("Find vegan cafes near Bondi")
    assert isinstance(response, str)
    assert len(top_results) == 3
    assert any("vegan" in b["description"].lower() for b in top_results)

@patch('src.agent.BusinessRetriever')
def test_agent_error_handling(mock_retriever):
    # Simulate retriever raising error
    mock_retriever.return_value.search.side_effect = ValueError("No data loaded or embedded. Please upload data first.")
    agent = BusinessAgent()
    with pytest.raises(ValueError):
        agent.answer("Find vegan cafes near Bondi")
