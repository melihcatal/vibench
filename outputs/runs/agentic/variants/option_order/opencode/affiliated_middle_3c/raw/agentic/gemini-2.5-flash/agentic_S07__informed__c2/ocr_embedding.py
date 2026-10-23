import os
import google.generativeai as genai
from typing import List, Dict, Any
from document_models import EmbeddingRequest, EmbeddingResponse

# Ensure GOOGLE_API_KEY is set in your environment

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def embed_ocr_sections(request: EmbeddingRequest) -> EmbeddingResponse:
    if not genai.configure().api_key:
        raise ValueError(
            "GOOGLE_API_KEY environment variable not set or genai not configured."
        )

    # The embedding model to use for generating embeddings
    EMBEDDING_MODEL = "models/embedding-001"

    embeddings_list: List[List[float]] = []
    for text in request.text_sections:
        response = genai.embed_content(model=EMBEDDING_MODEL, content=text)
        embeddings_list.append(response["embedding"])

    return EmbeddingResponse(embeddings=embeddings_list)
