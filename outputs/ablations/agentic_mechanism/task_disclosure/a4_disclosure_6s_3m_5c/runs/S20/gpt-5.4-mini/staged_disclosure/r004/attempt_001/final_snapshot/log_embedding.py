import json
import os
from typing import Iterable, List, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _selected_messages(log_messages: Sequence[str], limit: int = 100) -> List[str]:
    selected: List[str] = []
    for message in log_messages:
        if message is None:
            continue
        text = str(message).strip()
        if not text:
            continue
        selected.append(text)
        if len(selected) >= limit:
            break
    return selected


def embed_log_messages(log_messages: Sequence[str], limit: int = 100) -> List[List[float]]:
    client = OpenAI()
    selected = _selected_messages(log_messages, limit=limit)
    if not selected:
        return []
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=selected)
    return [item.embedding for item in response.data]


def embed_log_messages_from_json(log_messages_json: str, limit: int = 100) -> List[List[float]]:
    messages = json.loads(log_messages_json)
    if not isinstance(messages, Iterable):
        raise TypeError("log_messages_json must decode to an iterable of messages")
    return embed_log_messages(list(messages), limit=limit)
