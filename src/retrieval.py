import os
import json
import numpy as np
from src.config import settings
import openai
import faiss
from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings

class BusinessRetriever:
    """
    Loads business data, and enables fast semantic search with FAISS. Embedding is only performed on demand.
    """
    def __init__(self, data_path=None, embedding_model=None):
        """
        Initialize the BusinessRetriever. Does not embed or build index at startup.

        Args:
            data_path (str, optional): Path to the business dataset JSON file.
            embedding_model (str, optional): OpenAI embedding model name.
        """
        self.data_path = data_path or settings.DATA_PATH
        self.embedding_model = embedding_model or settings.EMBEDDING_MODEL
        self.businesses = []
        self.embeddings = None
        self.index = None
        self.id_map = None

    def _get_embeddings(self):
        """
        Return an OpenAIEmbeddings or AzureOpenAIEmbeddings instance as appropriate.
        """
        if settings.AZURE_OPENAI_ENDPOINT and settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT and settings.AZURE_OPENAI_KEY:
            return AzureOpenAIEmbeddings(
                azure_deployment=settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
                openai_api_key=settings.AZURE_OPENAI_KEY,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                openai_api_version=settings.AZURE_OPENAI_API_VERSION,
            )
        else:
            return OpenAIEmbeddings(
                model=self.embedding_model,
                openai_api_key=settings.OPENAI_API_KEY
            )

    def load_and_embed(self, data):
        """
        Accepts a list of business dicts, embeds them, and builds the FAISS index.

        Args:
            data (list): List of business dictionaries to be embedded and indexed.
        """
        self.businesses = data
        self.embeddings = self._get_embeddings()
        texts = [self._business_to_text(b) for b in self.businesses]
        vectors = self.embeddings.embed_documents(texts)
        vectors = np.array(vectors, dtype=np.float32)
        dim = vectors.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(vectors)
        self.id_map = {i: b for i, b in enumerate(self.businesses)}

    def _business_to_text(self, business):
        """
        Convert a business dict to a single string for embedding.

        Args:
            business (dict): Business dictionary.
        Returns:
            str: Concatenated business info.
        """
        return f"{business['name']} {business['category']} {business['location']} {business['description']}"

    def search(self, query, k=3):
        """
        Search for the top-k most relevant businesses for a query.

        Args:
            query (str): User's search query.
            k (int): Number of top results to return.
        Returns:
            list: Top-k business dicts ranked by semantic similarity.
        """
        if not self.index or not self.embeddings or not self.businesses:
            raise ValueError("No data loaded or embedded. Please upload data first.")
        q_vec = np.array([self.embeddings.embed_query(query)], dtype=np.float32)
        D, I = self.index.search(q_vec, k)
        return [self.id_map[i] for i in I[0] if i in self.id_map]
