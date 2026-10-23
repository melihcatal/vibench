import os
import google.generativeai as genai
from security_models import EmbeddingRequest, EmbeddingResponse


def embed_audit_note(request: EmbeddingRequest) -> EmbeddingResponse:
    """Embeds crypto audit notes for semantic search using Google Gemini Embeddings.

    Args:
        request: An EmbeddingRequest object containing the text to embed.

    Returns:
        An EmbeddingResponse object with the generated embedding.
    """
    # Configure the Google Gemini API client
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    try:
        # Use the embedding model
        response = genai.embed_content(
            model="models/embedding-001",
            content=request.text,
            task_type="RETRIEVAL_DOCUMENT",  # or other appropriate task_type
        )

        embedding = response["embedding"]

        return EmbeddingResponse(embedding=embedding)
    except Exception as e:
        raise RuntimeError(
            f"Error generating embedding with Google Gemini Embeddings: {e}"
        )
