from __future__ import annotations

import os
from typing import List

from openai import OpenAI


def embed_script(script: str) -> List[float]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model="text-embedding-3-small", input=script)
    return list(response.data[0].embedding)
