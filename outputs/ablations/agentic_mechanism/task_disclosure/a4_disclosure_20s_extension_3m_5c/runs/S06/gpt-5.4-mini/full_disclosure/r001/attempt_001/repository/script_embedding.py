from __future__ import annotations

import os
from typing import List, Optional

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-large"


def embed_script(text: str, model: str = DEFAULT_EMBEDDING_MODEL, api_key: Optional[str] = None) -> List[float]:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=text)
    return list(response.data[0].embedding)
