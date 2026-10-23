import os
from typing import List, Dict
from storage_client import StorageClient


def embed_text_with_gemini(
    texts: List[str], model_name: str = "models/embedding-001"
) -> List[List[float]]:
    """Generates embeddings for a list of texts using Google Gemini Embeddings API.

    Args:
        texts (List[str]): The list of texts to embed.
        model_name (str): The name of the embedding model to use (e.g., "models/embedding-001").

    Returns:
        List[List[float]]: A list of embedding vectors, one for each input text.
    """
    genai = StorageClient.get_generative_model_client()

    print(
        f"Sending embedding request to Gemini model {model_name} for {len(texts)} texts..."
    )
    response = genai.embed_content(
        model=model_name,
        content=texts,
    )

    embeddings = [embedding.values for embedding in response["embedding"]]

    print("Embedding generation complete.")
    return embeddings
