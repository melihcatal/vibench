from __future__ import annotations

from typing import List

from openai import OpenAI

PROVIDER = "openai"
MODEL_ID = "text-embedding-3-large"


def ocr_embedding(sections: List[str], api_key: str) -> List[List[float]]:
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model=MODEL_ID, input=sections)
    return [item.embedding for item in response.data]
