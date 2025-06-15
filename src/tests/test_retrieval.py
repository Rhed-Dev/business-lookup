import pytest
from unittest.mock import patch, MagicMock
from src.retrieval import BusinessRetriever

@patch('src.retrieval.BusinessRetriever._get_embeddings')
def test_retrieval(mock_get_embeddings):
    # Mock embeddings to return fixed vectors
    class DummyEmbeddings:
        def embed_documents(self, texts):
            return [[1.0, 2.0, 3.0]] * len(texts)
        def embed_query(self, query):
            return [1.0, 2.0, 3.0]
    mock_get_embeddings.return_value = DummyEmbeddings()
    retriever = BusinessRetriever()
    data = [
        {"name": "Vegan Cafe Bondi", "category": "Cafe", "location": "Bondi", "description": "A vegan cafe in Bondi."},
        {"name": "Green Eats", "category": "Restaurant", "location": "Bondi", "description": "Healthy vegan food."},
        {"name": "Plant Power", "category": "Diner", "location": "Bondi", "description": "Vegan burgers and shakes."}
    ]
    retriever.load_and_embed(data)
    results = retriever.search("vegan cafe Bondi", k=3)
    assert len(results) == 3
    assert any("vegan" in b["description"].lower() for b in results)

def test_retrieval_no_data():
    retriever = BusinessRetriever()
    with pytest.raises(ValueError):
        retriever.search("vegan cafe Bondi", k=3)
