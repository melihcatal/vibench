from translation_client import get_gemini_client
from translation_models import (
    TranslationMemoryEmbeddingRequest,
    TranslationMemoryEmbeddingResponse,
)
import google.generativeai as genai  # Explicitly import for identifiability
import os


def embed_translation_segment(
    request: TranslationMemoryEmbeddingRequest,
) -> TranslationMemoryEmbeddingResponse:
    genai = get_gemini_client()

    # The embedding model to use for Gemini
    model_name = "embedding-001"  # Concrete model identifier

    response = genai.embed_content(
        model=model_name,
        content=request.segment,
    )

    embedding_values = response["embedding"]

    return TranslationMemoryEmbeddingResponse(embedding=embedding_values)
