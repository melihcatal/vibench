from __future__ import annotations

import os
from typing import List

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-large"


def embed_script(text: str) -> List[float]:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return list(response.data[0].embedding)
