from embeddings_client import get_gemini_embeddings_client
from embeddings_models import normalize_embedding_response

def embed_text(text: str) -> list[float]:
    """
    Generates an embedding vector for a single text string using Google Gemini Embeddings.
    """
    client = get_gemini_embeddings_client()
    response = client.embed_content(model="embedding-001", content=text)
    return normalize_embedding_response(response)

if __name__ == '__main__':
    sample_text = "The quick brown fox jumps over the lazy dog."
    embedding = embed_text(sample_text)
    print(f"Embedding for \"{sample_text}\" (first 5 dimensions): {embedding[:5]}...")
    print(f"Embedding dimension: {len(embedding)}")
