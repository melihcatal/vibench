# embeddings_client.py
import os
import openai

class DirectEmbeddingsClient:
    """Simple wrapper around OpenAI's embeddings API for Direct Embeddings."""
    def __init__(self):
        # concrete provider: OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = api_key
        if not api_key:
            raise RuntimeError("OpenAI API key not found in environment variable OPENAI_API_KEY")

    def create_embedding(self, input, model="text-embedding-ada-002"):
        """Call OpenAI embeddings endpoint.

        Args:
            input (str or list[str]): text or list of texts.
            model (str): specific model identifier.

        Returns:
            dict: raw API response.
        """
        response = openai.Embedding.create(
            model=model,
            input=input
        )
        return response
