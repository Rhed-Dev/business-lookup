from pydantic import BaseModel
from typing import List, Any

class QueryRequest(BaseModel):
    """
    Request model for business query endpoint.

    Attributes:
        query (str): The user's search query.
    """
    query: str

class QueryResponse(BaseModel):
    """
    Response model for business query endpoint.

    Attributes:
        response (str): The LLM-generated response.
        top_results (List[Any]): List of top business results.
        followup (str | None): Optional follow-up suggestion.
    """
    response: str
    top_results: List[Any]
    followup: str | None = None
