from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_response


def embed_text(text: str) -> list[float]:
    """
    Generates an embedding vector for a single text string using Google Gemini Embeddings.
    """
    genai = get_embeddings_client()
    model = "models/embedding-001"  # Google Gemini Embeddings model identifier
    response = genai.embed_content(model=model, content=text)
    return normalize_embedding_response(response)


if __name__ == "__main__":
    sample_text = "This is a sample text for embedding."
    embedding = embed_text(sample_text)
    print(
        f"Embedding for '{sample_text}': {embedding[:5]}..."
    )  # Print first 5 elements
