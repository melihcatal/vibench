from __future__ import annotations

from typing import List

from openai import OpenAI

from document_models import EmbeddingResult, normalize_text


def embed_ocr_sections(sections: List[str], model: str = "text-embedding-3-large") -> EmbeddingResult:
    client = OpenAI()
    cleaned_sections = [normalize_text(section) for section in sections if normalize_text(section)]
    response = client.embeddings.create(model=model, input=cleaned_sections)
    vectors = [item.embedding for item in response.data]
    return EmbeddingResult(vectors=vectors, raw=response)
