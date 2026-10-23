from __future__ import annotations

import os
from typing import List

from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def platform_output_embedding(text: str) -> List[float]:
    client = OpenAI(api_key=OPENAI_API_KEY or None)
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return list(response.data[0].embedding)
