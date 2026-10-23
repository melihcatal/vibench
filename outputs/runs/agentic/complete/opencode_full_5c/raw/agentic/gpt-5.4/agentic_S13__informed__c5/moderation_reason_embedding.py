from __future__ import annotations

import os
from typing import List

from openai import OpenAI


def moderation_reason_embedding(rationales: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(
        model="text-embedding-3-large", input=rationales
    )
    return [list(item.embedding) for item in response.data]
