import os
import cohere
from speech_models import EmbeddingRequest, EmbeddingResponse


def get_transcript_embeddings(request: EmbeddingRequest) -> EmbeddingResponse:
    api_key = os.getenv("COHERE_API_KEY")
    co = cohere.Client(api_key)

    response = co.embed(
        texts=request.texts, model="embed-english-v3.0", input_type="search_document"
    )

    return EmbeddingResponse(embeddings=response.embeddings)
