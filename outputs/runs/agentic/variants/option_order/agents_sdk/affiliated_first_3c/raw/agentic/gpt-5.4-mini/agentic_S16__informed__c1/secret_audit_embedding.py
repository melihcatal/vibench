from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from security_models import join_lines


def embed_secret_audit_notes(notes: List[str], model: str = "text-embedding-3-small") -> List[float]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    text = join_lines(notes)
    response = client.embeddings.create(model=model, input=text)
    return list(response.data[0].embedding)
