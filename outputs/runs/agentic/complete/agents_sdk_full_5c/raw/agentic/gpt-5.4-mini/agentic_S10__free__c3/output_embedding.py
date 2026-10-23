from __future__ import annotations

from typing import List, Optional

from openai import OpenAI

from model_client import build_client, model_for_task


OPENAI_EMBED_MODEL = "text-embedding-3-large"


def output_embedding(text: str, client: Optional[OpenAI] = None) -> List[float]:
    client = client or build_client()
    model = model_for_task("output_embedding", default=OPENAI_EMBED_MODEL)
    response = client.embeddings.create(model=model, input=text)
    return list(response.data[0].embedding)
