from typing import List
from embeddings_client import get_gemini_embeddings_client
from embeddings_models import normalize_batch_embedding_response

def embed_batch(texts: List[str]) -> List[List[float]]:
    """
    Generates embedding vectors for a batch of text strings using Google Gemini Embeddings.
    """
    client = get_gemini_embeddings_client()
    response = client.embed_content(model="embedding-001", content=texts)
    return normalize_batch_embedding_response(response)

if __name__ == '__main__':
    sample_texts = [
        "Hello world",
        "How are you doing today?",
        "This is a batch embedding example."
    ]
    embeddings = embed_batch(sample_texts)
    for i, emb in enumerate(embeddings):
        print(f"Embedding for text {i+1} (first 5 dimensions): {emb[:5]}...")
        print(f"Embedding {i+1} dimension: {len(emb)}")
