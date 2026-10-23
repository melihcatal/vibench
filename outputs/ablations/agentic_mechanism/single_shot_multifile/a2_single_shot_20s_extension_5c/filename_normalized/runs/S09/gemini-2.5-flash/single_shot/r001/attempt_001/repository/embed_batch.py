import os
import cohere

def generate_embeddings_cohere(texts: list[str], model: str = "embed-english-v3.0") -> list[list[float]]:
    """
    Generates embeddings for a batch of text strings using Cohere.
    """
    co = cohere.Client(os.environ.get("COHERE_API_KEY"))
    try:
        response = co.embed(texts=texts, model=model)
        return response.embeddings
    except Exception as e:
        print(f"Error generating batch embeddings with Cohere: {e}")
        return []
