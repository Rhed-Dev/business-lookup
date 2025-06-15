from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Query
from pydantic import BaseModel
from src.agent import BusinessAgent
from src.followup import FollowUpAgent
from src.auth import verify_api_key
from src.chat_history import save_message, get_history
import logging
import json
import csv
from typing import List

app = FastAPI()

# Set up logger
logger = logging.getLogger("business_lookup_api")
logging.basicConfig(level=logging.INFO)

class QueryRequest(BaseModel):
    """Request model for business query endpoint."""
    query: str

class QueryResponse(BaseModel):
    """Response model for business query endpoint."""
    response: str
    top_results: list
    followup: str | None = None

business_agent = BusinessAgent()
followup_agent = FollowUpAgent()

@app.post("/query", response_model=QueryResponse, dependencies=[Depends(verify_api_key)])
def query_business(request: QueryRequest, session_id: str = Query(...)):
    """
    Handle POST /query. Returns LLM response, top results, and follow-up suggestion.
    Also saves the message to chat history.
    """
    try:
        response, top_results = business_agent.answer(request.query)
        followup = followup_agent.suggest(top_results)
        logger.info(f"Query: {request.query} | Top results: {top_results}")
        # Save to chat history
        save_message(session_id, {"role": "user", "content": request.query})
        save_message(session_id, {"role": "assistant", "content": response})
        return QueryResponse(response=response, top_results=top_results, followup=followup)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history", dependencies=[Depends(verify_api_key)])
def get_chat_history(session_id: str = Query(...)):
    """
    Retrieve chat history for a given session.
    """
    try:
        history = get_history(session_id)
        return {"session_id": session_id, "history": history}
    except Exception as e:
        logger.error(f"History error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload", dependencies=[Depends(verify_api_key)])
def upload_data(file: UploadFile = File(...)):
    """
    Upload a JSON or CSV file to embed and update the vector store.
    """
    try:
        if file.filename.endswith(".json"):
            data = json.load(file.file)
        elif file.filename.endswith(".csv"):
            reader = csv.DictReader((line.decode('utf-8') for line in file.file))
            data = list(reader)
        else:
            raise HTTPException(status_code=400, detail="Only .json or .csv files are supported.")
        # Update the retriever with new data and embed
        business_agent.retriever.load_and_embed(data)
        logger.info(f"Uploaded and embedded {len(data)} records from {file.filename}")
        return {"message": f"Uploaded and embedded {len(data)} records."}
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
