import os
import google.generativeai as genai  # Provider-identifying signal
from typing import List
from translation_models import EmbeddingRequest, EmbeddingResponse

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


def embed_segments(request: EmbeddingRequest) -> EmbeddingResponse:
    if not request.segments:
        return EmbeddingResponse(embeddings=[])

    result = genai.embed_content(
        model="models/embedding-001",  # Concrete model identifier
        content=request.segments,
        task_type="RETRIEVAL_DOCUMENT",
    )
    embeddings = [embedding for embedding in result["embedding"]]
    return EmbeddingResponse(embeddings=embeddings)
