from typing import List
from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_response


def embed_batch(texts: List[str]) -> List[List[float]]:
    """
    Generates embedding vectors for a batch of text strings using Google Gemini Embeddings.
    """
    genai = get_embeddings_client()
    model = "models/embedding-001"  # Google Gemini Embeddings model identifier
    response = genai.embed_content(model=model, content=texts)

    # The response for batch embedding is a list of embeddings
    embeddings = [normalize_embedding_response(item) for item in response.embeddings]
    return embeddings


if __name__ == "__main__":
    sample_texts = [
        "The quick brown fox jumps over the lazy dog.",
        "A stitch in time saves nine.",
        "Hello world!",
    ]
    batch_embeddings = embed_batch(sample_texts)
    for i, embedding in enumerate(batch_embeddings):
        print(
            f"Embedding for '{sample_texts[i]}': {embedding[:5]}..."
        )  # Print first 5 elements
