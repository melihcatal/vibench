from __future__ import annotations

import os
from typing import List

from openai import OpenAI


EMBED_MODEL = "text-embedding-3-large"


def embed_platform_output(text: str) -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.embeddings.create(model=EMBED_MODEL, input=text)
    return list(result.data[0].embedding)
