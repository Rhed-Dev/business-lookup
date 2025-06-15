import openai
from src.retrieval import BusinessRetriever
from src.config import settings

class BusinessAgent:
    """
    Main agent for answering business lookup queries using retrieval and LLM.
    Supports both OpenAI and Azure OpenAI endpoints.
    """
    def __init__(self):
        """
        Initialize the BusinessAgent with a retriever and LLM model from config.
        """
        self.retriever = BusinessRetriever()
        self.llm_model = settings.COMPLETIONS_MODEL
        self.azure_endpoint = settings.AZURE_OPENAI_ENDPOINT
        self.azure_deployment = settings.AZURE_OPENAI_DEPLOYMENT
        self.azure_api_version = settings.AZURE_OPENAI_API_VERSION
        self.azure_key = settings.AZURE_OPENAI_KEY
        self.use_azure = bool(self.azure_endpoint and self.azure_deployment and self.azure_key)

    def answer(self, query):
        """
        Retrieve top businesses and generate a natural language response using the LLM.
        The response will reference and include all top results.
        Supports both OpenAI and Azure OpenAI.

        Args:
            query (str): User's query.

        Returns:
            tuple[str, list]: LLM response and top business results.
        """
        top_results = self.retriever.search(query, k=3)
        context = "\n".join([
            f"{b['name']} ({b['category']}, {b['location']}): {b['description']}" for b in top_results
        ])
        prompt = (
            f"You are a helpful business lookup assistant.\n"
            f"User query: {query}\n"
            f"Relevant businesses (include all in your answer):\n{context}\n"
            f"Respond with a friendly, concise answer that mentions and summarizes ALL of the relevant businesses above."
        )
        if self.use_azure:
            client = openai.AzureOpenAI(
                api_key=self.azure_key,
                api_version=self.azure_api_version,
                azure_endpoint=self.azure_endpoint,
            )
            response = client.chat.completions.create(
                model=self.azure_deployment,
                messages=[{"role": "system", "content": prompt}]
            )
        else:
            response = openai.chat.completions.create(
                model=self.llm_model,
                messages=[{"role": "system", "content": prompt}]
            )
        return response.choices[0].message.content, top_results
