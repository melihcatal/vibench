import os
import google.generativeai as genai
from embeddings_client import get_embeddings_model

def embed_batch(texts: list[str]) -> list[list[float]]:
    """
    Generates embedding vectors for a batch of text strings using the Gemini embeddings model.
    """
    model = get_embeddings_model()
    response = model.embed_content(content=texts)
    return [e.values for e in response.embeddings]

if __name__ == "__main__":
    # Ensure GOOGLE_API_KEY is set in your environment
    sample_texts = [
        "Hello, world!",
        "Gemini API provides powerful embeddings.",
        "Batch processing is efficient."
    ]
    embeddings = embed_batch(sample_texts)
    for i, emb in enumerate(embeddings):
        print(f"Embedding for text {i+1} (first 5 dimensions): {emb[:5]}...")
        print(f"Embedding {i+1} dimension: {len(emb)}")
