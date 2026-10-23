import cohere
import os
from typing import List
from document_models import EmbeddingResponse


def embed_document_sections(sections: List[str]) -> List[EmbeddingResponse]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY must be set in the environment.")

    co = cohere.Client(api_key)
    response = co.embed(texts=sections, model="embed-english-v3.0")

    return [
        EmbeddingResponse(embedding=embedding, section=section)
        for embedding, section in zip(response.embeddings, sections)
    ]