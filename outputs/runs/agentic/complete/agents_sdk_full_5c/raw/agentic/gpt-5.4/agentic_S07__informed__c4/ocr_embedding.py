from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from document_models import normalize_text


def embed_document_sections(sections: Iterable[str], model: str = "text-embedding-3-large") -> dict:
    cleaned_sections: List[str] = [normalize_text(section) for section in sections if normalize_text(section)]
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(
        model=model,
        input=cleaned_sections,
    )
    return {
        "provider": "openai",
        "model": model,
        "embeddings": [item.embedding for item in response.data],
        "dimensions": len(response.data[0].embedding) if response.data else 0,
    }
