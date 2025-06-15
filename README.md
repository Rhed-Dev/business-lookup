# Business Lookup Assistant

## Overview
Business Lookup Assistant is a Retrieval-Augmented Generation (RAG) API that uses LLMs (OpenAI or Azure OpenAI) to answer natural language queries about local businesses. It supports semantic search over a business dataset, chat history per session, and secure API key authentication with rate limiting. Built with FastAPI and FAISS.

## Features
- Query businesses using natural language (POST `/query`)
- Returns LLM-generated response, top 3 relevant businesses, and a follow-up suggestion
- Upload new business data (JSON or CSV) via POST `/upload` to update the vector store
- Retrieve chat history for a session (GET `/history`)
- Supports both OpenAI and Azure OpenAI for embeddings and completions
- API key authentication and per-key rate limiting
- Persistent chat history (JSON file)
- Dockerfile and tests included

## Setup Instructions
0. **Clone the repository**
   ```bash
   git clone https://github.com/Rhed-Dev/business-lookup.git
   cd business-lookup
   ```
1. **Create a Python environment (recommended)**
   - Using Conda:
     ```bash
     conda create -n business-lookup python=3.11
     conda activate business-lookup
     ```
   - Or with venv:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate  # On Windows
     source .venv/bin/activate  # On macOS/Linux
     ```
   - Or use VS Code's built-in environment manager.

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set environment variables**
   - `OPENAI_API_KEY` (for OpenAI)
   - `API_KEY` (for your API authentication, default: `test-api-key`)
   - (Optional for Azure) `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_KEY`, `AZURE_OPENAI_DEPLOYMENT`, etc.
   - Example (Windows):
     ```cmd
     set OPENAI_API_KEY=your-key-here
     set API_KEY=your-api-key
     ```
4. **Run the API
   - For development/debugging (with Uvicorn):
     ```bash
     uvicorn src.main:app --reload
     ```
   - For deployment or isolation (with Docker):
     ```bash
     docker build -t business-lookup .
     docker run -p 8000:8000 --env-file .env business-lookup
     ```
5. **Query the API**
   - POST `/query?session_id=123` with `{ "query": "Find vegan cafes near Bondi" }` and header `Authorization: Bearer <API_KEY>`
   - GET `/history?session_id=123` to retrieve chat history
   - POST `/upload` with a JSON or CSV file to update data

## Environment Variables & .env Setup

You can use a `.env` file to manage your environment variables. Copy the provided `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

**.env variables:**
- `OPENAI_API_KEY` (required for OpenAI)
- `API_KEY` (required for API authentication) - use you may use default value 'test-api-key'
- `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_KEY`, `AZURE_OPENAI_DEPLOYMENT`, etc. (optional, for Azure OpenAI)
- `DATA_PATH`, `EMBEDDING_MODEL`, `COMPLETIONS_MODEL` (optional overrides)

> The app will automatically load variables from `.env` if present.

## File Structure
- `data/business.json` - Example business dataset
- `data/chat_history.json` - Persistent chat history
- `src/main.py` - FastAPI app and endpoints
- `src/agent.py` - LLM agent (OpenAI/Azure support)
- `src/retrieval.py` - Embedding, FAISS vector search, data loading
- `src/followup.py` - Follow-up suggestion agent
- `src/chat_history.py` - Chat history storage
- `src/auth.py` - API key and rate limiting
- `src/config.py` - Config and environment variables
- `src/models.py` - Pydantic models
- `src/tests/` - Pytest-based tests

---

**AI/ML Engineer JD**: This project demonstrates LLM integration, RAG, vector search, agent design, API security, and deployment. See code for details.
