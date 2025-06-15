# Business Lookup Assistant - README

## Overview
This project is an LLM-powered assistant that takes user input (e.g., “Find vegan cafes near Bondi”) and queries a mock business dataset using Retrieval-Augmented Generation (RAG) with semantic search. It uses OpenAI's `text-embedding-ada` for embeddings, FAISS for the local vector store, and OpenAI's GPT for response generation. Built with FastAPI.

## Features
- FastAPI endpoint for natural language business lookup
- Embeds a local JSON dataset using OpenAI embeddings
- Uses FAISS for fast vector similarity search
- Returns the top 3 most relevant businesses
- Generates a natural language response using OpenAI GPT
- (Bonus) Follows up with a second agent for directions or booking

## Setup Instructions
1. **Clone the repo & install dependencies**
   ```bash
   pip install fastapi uvicorn openai faiss-cpu langchain
   ```
2. **Set your OpenAI API key**
   ```bash
   export OPENAI_API_KEY=your-key-here
   ```
   (On Windows: `set OPENAI_API_KEY=your-key-here`)
3. **Run the API**
   ```bash
   uvicorn src.main:app --reload
   ```
4. **Query the API**
   - POST to `/query` with `{ "query": "Find vegan cafes near Bondi" }`

## File Structure
- `data/business.json` - Mock business dataset
- `src/main.py` - FastAPI app
- `src/agent.py` - LLM agent logic
- `src/retrieval.py` - Embedding & vector search logic
- `src/followup.py` - (Bonus) Follow-up agent
- `src/models.py` - Pydantic models
- `src/config.py` - Config & API keys
- `src/tests/` - Test files

## Extending
- Add more business data to `business.json`
- Swap OpenAI for other LLMs/embeddings in `retrieval.py`/`agent.py`
- Add more endpoints or agent behaviors

---

**AI/ML Engineer JD**: This project demonstrates LLM integration, RAG, vector search, agent design, and API deployment. See code for details.
