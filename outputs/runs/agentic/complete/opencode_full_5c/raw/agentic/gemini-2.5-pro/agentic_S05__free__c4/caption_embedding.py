from speech_client import get_generative_client
from speech_models import EmbeddingResponse
import google.generativeai as genai


def embed_caption_chunk(text: str) -> EmbeddingResponse:
    """
    Embeds a caption chunk for semantic search using Google's embedding model.

    Args:
        text: The caption text to embed.

    Returns:
        An EmbeddingResponse object with the embedding vector.
    """
    get_generative_client()  # Configures the API key

    result = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="RETRIEVAL_DOCUMENT",
    )

    return EmbeddingResponse(embedding=result["embedding"])


if __name__ == "__main__":
    caption = "The team discussed the quarterly budget and future hiring plans."
    embedding_response = embed_caption_chunk(caption)

    print(f"Original text: {caption}")
    print(f"Embedding vector (first 5 elements): {embedding_response.embedding[:5]}")
    print(f"Embedding vector dimension: {len(embedding_response.embedding)}")
