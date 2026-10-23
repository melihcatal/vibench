import os
from typing import Iterable, List, Sequence

from openai import OpenAI


def embed_log_messages(messages: Sequence[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=list(messages))
    return [item.embedding for item in response.data]


def embed_selected_log_messages(messages: Iterable[str]) -> List[List[float]]:
    return embed_log_messages(list(messages))
