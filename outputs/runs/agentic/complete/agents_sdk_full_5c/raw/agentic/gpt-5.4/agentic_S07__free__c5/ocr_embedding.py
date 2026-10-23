from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI


PROVIDER = "openai"
MODEL = "text-embedding-3-large"


def ocr_embedding(sections: Iterable[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    payload = list(sections)
    if not payload:
        return []
    response = client.embeddings.create(model=MODEL, input=payload)
    return [item.embedding for item in response.data]
