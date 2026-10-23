from __future__ import annotations

import os
from typing import List

from openai import OpenAI


MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_script(script: str) -> List[float]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model=MODEL, input=script)
    return list(response.data[0].embedding)
