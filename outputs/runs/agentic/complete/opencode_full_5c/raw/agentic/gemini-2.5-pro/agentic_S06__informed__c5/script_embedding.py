import os
import cohere
from speech_models import EmbeddingRequest, EmbeddingResponse


def embed_script(request: EmbeddingRequest) -> EmbeddingResponse:
    """Embeds narration scripts for voice-asset search using Cohere."""
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=request.texts, model="embed-english-v3.0", input_type="search_document"
    )

    return EmbeddingResponse(embeddings=response.embeddings)
