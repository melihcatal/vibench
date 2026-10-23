from __future__ import annotations

import os
from typing import List

from openai import OpenAI


def log_embedding(message_text: str) -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=message_text,
    )
    return response.data[0].embedding
