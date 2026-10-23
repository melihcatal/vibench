import os
from typing import List
import cohere
from speech_models import EmbeddingRequest, EmbeddingResponse


def transcript_embedding(texts: List[str]) -> EmbeddingResponse:
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(
        texts=texts, model="embed-english-v3.0", input_type="search_document"
    )
    return EmbeddingResponse(embeddings=response.embeddings)
