from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from speech_models import normalize_text


def embed_script(text: str, model: str = "text-embedding-3-small") -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.embeddings.create(model=model, input=normalize_text(text))
    return list(result.data[0].embedding)
