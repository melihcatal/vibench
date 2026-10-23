import os
from typing import Any, List

from openai import OpenAI

from safety_client import get_openai_client, normalize_text_input


def moderation_reason_embedding(reason: Any) -> List[float]:
    client: OpenAI = get_openai_client()
    response = client.embeddings.create(
        model=os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        input=normalize_text_input(reason),
    )
    return list(response.data[0].embedding)
