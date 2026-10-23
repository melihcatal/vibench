import os
from typing import Any, Dict, Iterable, List, Optional, Sequence

from openai import OpenAI


DEFAULT_OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _get_client(api_key: Optional[str] = None) -> OpenAI:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=key)


def _normalize_sections(sections: Sequence[Any]) -> List[str]:
    normalized: List[str] = []
    for section in sections:
        if section is None:
            continue
        if isinstance(section, str):
            text = section.strip()
        elif isinstance(section, dict):
            for key in ("text", "content", "value", "body"):
                if key in section and section[key]:
                    text = str(section[key]).strip()
                    break
            else:
                text = str(section).strip()
        else:
            text = str(section).strip()
        if text:
            normalized.append(text)
    return normalized


def embed_document_sections(
    sections: Sequence[Any],
    *,
    model: str = DEFAULT_OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    texts = _normalize_sections(sections)
    client = _get_client(api_key=api_key)
    response = client.embeddings.create(model=model, input=texts)
    embeddings = [item.embedding for item in response.data]
    return {
        "model": model,
        "provider": "openai",
        "count": len(texts),
        "texts": texts,
        "embeddings": embeddings,
    }


def embed_document_sections_iter(
    sections: Iterable[Any],
    *,
    model: str = DEFAULT_OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    return embed_document_sections(list(sections), model=model, api_key=api_key)
