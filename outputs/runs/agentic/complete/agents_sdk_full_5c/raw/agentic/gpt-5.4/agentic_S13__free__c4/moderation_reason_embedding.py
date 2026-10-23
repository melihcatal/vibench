from __future__ import annotations

import os
from typing import List

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-small"


def moderation_reason_embedding(reason_text: str) -> List[float]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=reason_text,
    )
    return response.data[0].embedding
