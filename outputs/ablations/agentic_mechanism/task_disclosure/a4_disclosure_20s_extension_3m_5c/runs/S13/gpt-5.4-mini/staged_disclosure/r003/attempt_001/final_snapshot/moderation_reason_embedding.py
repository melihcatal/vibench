import os
from typing import Iterable, List, Sequence

from openai import OpenAI


MODEL_ID = "text-embedding-3-small"


def _client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def embed_moderation_rationales(rationales: Sequence[str]) -> List[List[float]]:
    texts = [r.strip() for r in rationales if r and r.strip()]
    if not texts:
        return []
    client = _client()
    response = client.embeddings.create(model=MODEL_ID, input=texts)
    return [item.embedding for item in response.data]


def embed_moderation_reason(reason: str) -> List[float]:
    embeddings = embed_moderation_rationales([reason])
    return embeddings[0] if embeddings else []


def batch_embed_cases(cases: Iterable[dict], reason_key: str = "moderation_reason") -> List[dict]:
    items = list(cases)
    reasons = [str(case.get(reason_key, "")) for case in items]
    embeddings = embed_moderation_rationales(reasons)
    embedded_cases = []
    embedding_index = 0
    for case in items:
        reason = str(case.get(reason_key, "")).strip()
        if reason:
            case = dict(case)
            case["moderation_reason_embedding"] = embeddings[embedding_index]
            embedding_index += 1
        embedded_cases.append(case)
    return embedded_cases
