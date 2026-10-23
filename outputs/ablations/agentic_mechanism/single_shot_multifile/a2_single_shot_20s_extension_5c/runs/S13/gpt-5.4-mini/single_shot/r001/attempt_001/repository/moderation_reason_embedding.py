from typing import Any, Dict, Iterable, List
from openai import OpenAI
from safety_client import get_openai_client

EMBEDDING_MODEL = "text-embedding-3-small"


def moderation_reason_embedding(reasons: Iterable[str], *, model: str | None = None) -> Dict[str, Any]:
    client: OpenAI = get_openai_client()
    chosen_model = model or EMBEDDING_MODEL
    items = [reason if reason is not None else "" for reason in reasons]
    response = client.embeddings.create(model=chosen_model, input=items)
    vectors: List[List[float]] = [list(entry.embedding) for entry in response.data]
    return {"embeddings": vectors, "model": chosen_model}


if __name__ == "__main__":
    raise SystemExit(0)
