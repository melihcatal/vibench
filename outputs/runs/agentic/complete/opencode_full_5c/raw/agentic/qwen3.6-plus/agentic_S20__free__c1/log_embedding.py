import os
import json
from typing import List, Dict, Any, Optional

from openai import OpenAI

from fetch_recent_logs import fetch_recent_logs
from observability_models import LogEntry


OPENAI_MODEL = "gpt-4o"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def embed_log_message(
    message: str,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> Dict[str, Any]:
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.embeddings.create(
        model=model,
        input=message,
        encoding_format="float",
    )

    embedding = response.data[0].embedding

    return {
        "embedding": embedding,
        "model_used": model,
        "text_length": len(message),
        "embedding_dimension": len(embedding),
    }


def embed_log_messages(
    messages: List[str],
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[Dict[str, Any]]:
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.embeddings.create(
        model=model,
        input=messages,
        encoding_format="float",
    )

    results = []
    for i, item in enumerate(response.data):
        results.append(
            {
                "index": i,
                "embedding": item.embedding,
                "model_used": model,
                "text_length": len(messages[i]) if i < len(messages) else 0,
                "embedding_dimension": len(item.embedding),
            }
        )

    return results


def embed_recent_log_messages(
    service: Optional[str] = None,
    level: Optional[str] = None,
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    limit: int = 10,
    model: str = OPENAI_EMBEDDING_MODEL,
    field_filters: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    response = fetch_recent_logs(
        service=service,
        level=level,
        time_from=time_from,
        time_to=time_to,
        limit=limit,
        field_filters=field_filters,
    )

    messages = [entry.message for entry in response.entries]
    embeddings = embed_log_messages(messages, model=model)

    results = []
    for i, entry in enumerate(response.entries):
        if i < len(embeddings):
            emb = embeddings[i]
            results.append(
                {
                    "log_id": entry.id,
                    "timestamp": entry.timestamp,
                    "service": entry.service,
                    "hostname": entry.hostname,
                    "message": entry.message,
                    "embedding": emb["embedding"],
                    "model_used": emb["model_used"],
                    "embedding_dimension": emb["embedding_dimension"],
                }
            )

    return results


def compute_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


if __name__ == "__main__":
    test_messages = [
        "Connection refused: unable to reach database server at db-primary:5432",
        "Database connection pool exhausted, all connections in use",
        "Request timeout after 30000ms for endpoint /api/v2/users",
    ]
    results = embed_log_messages(test_messages)
    for r in results:
        print(
            f"Message {r['index']}: dimension={r['embedding_dimension']}, model={r['model_used']}"
        )
