from __future__ import annotations

import os
from typing import List

from openai import OpenAI


def log_embedding(text: str) -> List[float]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text,
    )
    return list(response.data[0].embedding)
