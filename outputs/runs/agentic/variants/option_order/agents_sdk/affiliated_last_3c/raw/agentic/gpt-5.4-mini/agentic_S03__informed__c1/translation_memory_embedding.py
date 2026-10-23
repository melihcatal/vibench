from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from translation_models import TranslationMemoryEmbedding, normalize_text

PROVIDER_NAME = "OpenAI"
MODEL_ID = "text-embedding-3-small"


def embed_translation_memory(segment: str) -> TranslationMemoryEmbedding:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    normalized = normalize_text(segment)
    response = client.embeddings.create(model=MODEL_ID, input=normalized)
    vector = list(response.data[0].embedding)
    return TranslationMemoryEmbedding(provider=PROVIDER_NAME, segment=normalized, vector=vector)
