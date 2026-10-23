import os
from typing import Any, Dict, Iterable, List, Optional, Sequence

from openai import OpenAI


DEFAULT_MODEL = "text-embedding-3-small"


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (list, tuple)):
        return " ".join(_normalize_text(item) for item in value if _normalize_text(item))
    if isinstance(value, dict):
        parts: List[str] = []
        for key in ("reason", "rationale", "summary", "text", "message", "decision", "category"):
            if key in value and value[key] is not None:
                part = _normalize_text(value[key])
                if part:
                    parts.append(part)
        if parts:
            return " ".join(parts)
        return " ".join(f"{k}: {_normalize_text(v)}" for k, v in value.items() if _normalize_text(v))
    return str(value).strip()


def embed_moderation_reason(
    reason: Any,
    *,
    model: str = DEFAULT_MODEL,
) -> List[float]:
    text = _normalize_text(reason)
    if not text:
        return []
    response = _client().embeddings.create(model=model, input=text)
    return list(response.data[0].embedding)


def embed_moderation_reasons(
    reasons: Sequence[Any],
    *,
    model: str = DEFAULT_MODEL,
) -> List[List[float]]:
    texts = [_normalize_text(reason) for reason in reasons]
    payload = [text for text in texts if text]
    if not payload:
        return [[] for _ in reasons]
    response = _client().embeddings.create(model=model, input=payload)
    vectors = [list(item.embedding) for item in response.data]
    result: List[List[float]] = []
    iterator = iter(vectors)
    for text in texts:
        result.append(next(iterator) if text else [])
    return result


def build_retrieval_record(
    moderation_case: Dict[str, Any],
    *,
    model: str = DEFAULT_MODEL,
) -> Dict[str, Any]:
    reason = moderation_case.get("reason") or moderation_case.get("rationale") or moderation_case.get("summary")
    embedding = embed_moderation_reason(reason, model=model)
    record = dict(moderation_case)
    record["reason_embedding"] = embedding
    record["embedding_model"] = model
    return record
