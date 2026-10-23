import os
from typing import List

from document_models import TextExtractionResult

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def embed_document_sections(text_result: TextExtractionResult) -> List[List[float]]:
    from openai import OpenAI

    if not OPENAI_API_KEY:
        raise RuntimeError("OpenAI API key is required")
    client = OpenAI()
    sections = [section.strip() for section in text_result.text.split("\n\n") if section.strip()]
    if not sections:
        sections = [text_result.text]
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=sections)
    return [item.embedding for item in response.data]
