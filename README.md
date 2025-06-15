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
   - Please use the `.env` file for all environment variables. Copy `.env.example` to `.env` and fill in your keys:
     ```bash
     cp .env.example .env
     # Then edit .env with your preferred editor
     ```
   - The app will automatically load variables from `.env` if present.
   - (Manual setting of environment variables is not required unless you have a special use case.)
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

## How to Use the API

> **Important:** All endpoints require Bearer token authentication. By default, the API key is `test-api-key` (as set in your `.env` or environment variables). Please use this value unless you have changed it.

### 1. Upload Data (Required Before Querying)
- Endpoint: `POST /upload`
- **Authorization:** Kindly set the `Authorization` header to `Bearer test-api-key` (or your custom API key).
- **Instructions:**
  - **Postman:**
    1. Set the method to POST and the URL to `http://localhost:8000/upload`.
    2. Go to the Authorization tab, select `Bearer Token`, and enter `test-api-key` (or your custom key).
    3. In Body, select `form-data`.
    4. Add a key named `file`, set type to `File`, and upload your business JSON or CSV file.
    5. Click Send to upload.
  - **FastAPI Docs:**
    1. Open `http://localhost:8000/docs` in your browser.
    2. Click `Authorize` (top right) and enter `test-api-key` (no need to type 'Bearer ').
    3. Expand the `/upload` endpoint, click `Try it out`.
    4. Click `Choose File` and select your business JSON or CSV file.
    5. Click Execute to upload.
- **Note:** Mock business data is already provided for you in `data/business.json`. You may use this file for your initial upload or testing.
- Please ensure you upload data before making any queries.

### 2. Query Businesses
- Endpoint: `POST /query?session_id=YOUR_SESSION_ID`
- **Authorization:** Kindly set the `Authorization` header to `Bearer test-api-key` (or your custom API key).
- **Body (sample query):**
  ```json
  { "query": "Find vegan cafes near Bondi" }
  ```
- **How to test:**
  - **Postman:**
    1. Set the method to POST and the URL to `http://localhost:8000/query?session_id=test123`.
    2. Go to the Authorization tab, select `Bearer Token`, and enter `test-api-key` (or your custom key).
    3. In Body, select `raw` and `JSON`, then enter your query JSON (see sample above).
    4. Click Send and kindly view the response.
  - **FastAPI Docs:**
    1. Open `http://localhost:8000/docs` in your browser.
    2. Click `Authorize` and enter `test-api-key` (no need to type 'Bearer ').
    3. Expand the `/query` endpoint, click `Try it out`, fill in the session ID and query, then execute.

### 3. Get Chat History
- Endpoint: `GET /history?session_id=YOUR_SESSION_ID`
- **Authorization:** Kindly set the `Authorization` header to `Bearer test-api-key` (or your custom API key).
- **How to test:**
  - **Postman:**
    1. Set the method to GET and the URL to `http://localhost:8000/history?session_id=test123`.
    2. Go to the Authorization tab, select `Bearer Token`, and enter `test-api-key` (or your custom key).
    3. Click Send to kindly retrieve the chat history for the session.
  - **FastAPI Docs:**
    1. Open `http://localhost:8000/docs`.
    2. Click `Authorize` and enter `test-api-key` (no need to type 'Bearer ').
    3. Expand the `/history` endpoint, click `Try it out`, enter the session ID, and execute.

> **Reminder:** The default API key is `test-api-key`. Please update your `.env` if you wish to use a different key. Always upload your business data before querying or retrieving chat history.

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
