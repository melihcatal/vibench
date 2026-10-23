from __future__ import annotations

import os
from openai import OpenAI


def platform_output_embedding(text: str) -> list[float]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    result = client.embeddings.create(model="text-embedding-3-small", input=text)
    return result.data[0].embedding
