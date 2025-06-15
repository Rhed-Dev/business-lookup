import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Loads configuration from environment variables or defaults.
    """
    def __init__(self):
        self.OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
        self.DATA_PATH: str = os.getenv("DATA_PATH", "data/business.json")
        self.EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
        self.COMPLETIONS_MODEL: str = os.getenv("COMPLETIONS_MODEL", "gpt-4.1-nano")
        self.API_KEY: str = os.getenv("API_KEY", "test-api-key")
        # Azure OpenAI support
        self.AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        self.AZURE_OPENAI_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1-nano")
        self.AZURE_OPENAI_KEY: str = os.getenv("AZURE_OPENAI_KEY", "")
        self.AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")

settings = Settings()