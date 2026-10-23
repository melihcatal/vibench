from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from document_models import normalize_text


def embed_document_sections(sections: List[str], model: str = "text-embedding-3-large") -> List[List[float]]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    client = OpenAI(api_key=api_key)
    cleaned_sections = [normalize_text(section) for section in sections]
    response = client.embeddings.create(model=model, input=cleaned_sections)
    return [item.embedding for item in response.data]
