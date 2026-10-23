from typing import List
from model_client import get_model_client

def generate_embeddings(text: str) -> List[float]:
    """
    Generates embeddings for Azure OpenAI model output using text-embedding-ada-002.
    """
    client = get_model_client()
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding