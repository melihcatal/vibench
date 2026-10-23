import os
from typing import List

try:
    from openai import OpenAI
except ImportError:
    raise ImportError("The 'openai' library is not installed. Please install it using 'pip install openai'")

class EmbeddingsClient:
    def __init__(self, api_key: str = None, base_url: str = None, model: str = "text-embedding-ada-002"):
        """
        Initializes the EmbeddingsClient for OpenAI embeddings.

        Args:
            api_key: The OpenAI API key. If not provided, it will be fetched from OPENAI_API_KEY environment variable.
            base_url: The base URL for the OpenAI API.
            model: The name of the OpenAI embeddings model to use.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set it as an environment variable 'OPENAI_API_KEY' or pass it during initialization.")
        self.client = OpenAI(api_key=self.api_key, base_url=base_url)
        self.model = model

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of texts using the configured OpenAI model.

        Args:
            texts: A list of strings for which to generate embeddings.

        Returns:
            A list of lists of floats, where each inner list is the embedding for the corresponding text.
        """
        response = self.client.embeddings.create(input=texts, model=self.model)
        embeddings = [data.embedding for data in response.data]
        return embeddings

