import os
from typing import Optional

from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
EMBEDDING_MODEL = "text-embedding-3-small"


def embed_moderation_rationale(
    rationale: str,
    case_id: Optional[str] = None,
) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=rationale,
    )

    embedding = response.data[0].embedding

    result = {
        "rationale": rationale,
        "embedding": embedding,
        "dimensions": len(embedding),
        "model": EMBEDDING_MODEL,
        "provider": "openai",
    }
    if case_id:
        result["case_id"] = case_id

    return result


def embed_batch_rationales(
    rationales: list[dict],
) -> list[dict]:
    client = OpenAI(api_key=OPENAI_API_KEY)

    texts = []
    metadata = []
    for item in rationales:
        if isinstance(item, str):
            texts.append(item)
            metadata.append({})
        else:
            texts.append(item.get("rationale", ""))
            metadata.append(item)

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )

    results = []
    for i, data in enumerate(response.data):
        entry = {
            "rationale": texts[i],
            "embedding": data.embedding,
            "dimensions": len(data.embedding),
            "model": EMBEDDING_MODEL,
            "provider": "openai",
        }
        if metadata[i].get("case_id"):
            entry["case_id"] = metadata[i]["case_id"]
        results.append(entry)

    return results


def compute_rationale_similarity(
    rationale_a: str,
    rationale_b: str,
) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[rationale_a, rationale_b],
    )

    vec_a = response.data[0].embedding
    vec_b = response.data[1].embedding

    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    similarity = dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    return {
        "similarity": round(similarity, 4),
        "model": EMBEDDING_MODEL,
        "provider": "openai",
    }
