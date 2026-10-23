import os
from typing import Iterable, List, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _normalize_log_message(message: str) -> str:
    return " ".join(message.strip().split())


def select_log_messages(log_messages: Sequence[str], max_messages: int = 100) -> List[str]:
    selected = []
    for message in log_messages:
        normalized = _normalize_log_message(message)
        if normalized:
            selected.append(normalized)
        if len(selected) >= max_messages:
            break
    return selected


def embed_log_messages(log_messages: Sequence[str], model: str = OPENAI_EMBEDDING_MODEL) -> List[List[float]]:
    client = OpenAI()
    selected_messages = select_log_messages(log_messages)
    if not selected_messages:
        return []
    response = client.embeddings.create(model=model, input=selected_messages)
    return [item.embedding for item in response.data]


def embed_selected_log_messages(log_messages: Iterable[str], max_messages: int = 100, model: str = OPENAI_EMBEDDING_MODEL) -> List[List[float]]:
    return embed_log_messages(select_log_messages(list(log_messages), max_messages=max_messages), model=model)
