import os
from openai import OpenAI  # Provider SDK import


def get_embedding(text: str) -> list[float]:
    """
    Embeds model outputs for clustering or retrieval using OpenAI Embeddings.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )  # Provider-specific environment variable
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small",  # Provider-specific model ID
    )
    return response.data[0].embedding
