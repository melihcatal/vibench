from __future__ import annotations

import os
from typing import List

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_script(text: str) -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text)
    return list(response.data[0].embedding)
