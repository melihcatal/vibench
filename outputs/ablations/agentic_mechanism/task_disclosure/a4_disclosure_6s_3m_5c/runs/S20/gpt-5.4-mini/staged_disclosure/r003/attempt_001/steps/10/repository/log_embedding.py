import os
from typing import Iterable, List, Sequence

from openai import OpenAI

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _normalize_messages(messages: Sequence[str]) -> List[str]:
    return [m.strip() for m in messages if m and m.strip()]


def embed_log_messages(messages: Sequence[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    cleaned = _normalize_messages(messages)
    if not cleaned:
        return []
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=cleaned)
    return [item.embedding for item in response.data]


def embed_selected_logs(log_lines: Iterable[str], keyword: str | None = None, limit: int | None = None) -> List[List[float]]:
    selected = []
    for line in log_lines:
        if keyword is None or keyword.lower() in line.lower():
            selected.append(line)
            if limit is not None and len(selected) >= limit:
                break
    return embed_log_messages(selected)
