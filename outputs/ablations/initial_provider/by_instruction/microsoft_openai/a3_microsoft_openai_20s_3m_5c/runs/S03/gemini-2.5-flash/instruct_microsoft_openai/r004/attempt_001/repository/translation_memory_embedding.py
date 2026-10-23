import os
from typing import List
import openai

# Using a dedicated client for embeddings as it might use a different model/endpoint
class EmbeddingClient:
    def __init__(self):
        self.client = openai.AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2023-05-15", # Or the appropriate API version for embeddings
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        # This should be your deployed embedding model name
        self.embedding_model_name = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL_NAME", "text-embedding-ada-002")

def generate_embedding(text: str) -> List[float]:
    """
    Generates an embedding for a given text segment using OpenAI's embedding model.
    """
    embedding_client_manager = EmbeddingClient()
    client = embedding_client_manager.client
    model_name = embedding_client_manager.embedding_model_name

    response = client.embeddings.create(
        input=[text],
        model=model_name
    )
    return response.data[0].embedding
