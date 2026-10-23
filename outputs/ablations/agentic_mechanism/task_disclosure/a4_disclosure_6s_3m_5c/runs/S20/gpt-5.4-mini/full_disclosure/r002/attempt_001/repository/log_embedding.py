import os
from typing import Iterable, List, Sequence

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def _normalize_messages(messages: Sequence[str]) -> List[str]:
    normalized = [message.strip() for message in messages if message and message.strip()]
    if not normalized:
        raise ValueError("at least one non-empty log message is required")
    return normalized


def embed_log_messages(messages: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    normalized = _normalize_messages(messages)
    response = client.embeddings.create(model=model, input=normalized)
    return [item.embedding for item in response.data]


def embed_log_message(message: str, model: str = DEFAULT_EMBEDDING_MODEL) -> List[float]:
    return embed_log_messages([message], model=model)[0]
