import os
from typing import Iterable, List, Sequence

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_log_messages(messages: Sequence[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    selected = [m.strip() for m in messages if m and m.strip()]
    if not selected:
        return []
    response = _client().embeddings.create(model=model, input=selected)
    return [item.embedding for item in response.data]


def embed_selected_logs(log_messages: Iterable[str]) -> List[List[float]]:
    return embed_log_messages(list(log_messages))
