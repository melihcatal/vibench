import os
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass(frozen=True)
class ScriptEmbedding:
    text: str
    embedding: List[float]
    model: str = DEFAULT_EMBEDDING_MODEL


def _normalize_script(text: str) -> str:
    return " ".join(text.split()).strip()


def embed_script(
    text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> ScriptEmbedding:
    client_kwargs = {"api_key": api_key or os.getenv("OPENAI_API_KEY")}
    resolved_base_url = base_url or os.getenv("OPENAI_BASE_URL")
    if resolved_base_url is not None:
        client_kwargs["base_url"] = resolved_base_url
    client = OpenAI(**client_kwargs)
    normalized_text = _normalize_script(text)
    response = client.embeddings.create(model=model, input=normalized_text)
    return ScriptEmbedding(text=normalized_text, embedding=list(response.data[0].embedding), model=model)


def embed_scripts(
    texts: Sequence[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> List[ScriptEmbedding]:
    client_kwargs = {"api_key": api_key or os.getenv("OPENAI_API_KEY")}
    resolved_base_url = base_url or os.getenv("OPENAI_BASE_URL")
    if resolved_base_url is not None:
        client_kwargs["base_url"] = resolved_base_url
    client = OpenAI(**client_kwargs)
    normalized_texts = [_normalize_script(text) for text in texts]
    response = client.embeddings.create(model=model, input=normalized_texts)
    return [
        ScriptEmbedding(text=normalized_texts[idx], embedding=list(item.embedding), model=model)
        for idx, item in enumerate(response.data)
    ]
