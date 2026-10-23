from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from document_models import EmbeddingResult, normalize_text


def embed_document_sections(sections: List[str], model: str = "text-embedding-3-large") -> EmbeddingResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    inputs = [normalize_text(section) for section in sections]
    response = client.embeddings.create(model=model, input=inputs)
    vectors = [item.embedding for item in response.data]
    return EmbeddingResult(vectors=vectors, raw=response)
