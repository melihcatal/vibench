from safety_client import get_openai_client, EMBEDDING_MODEL


def embed_moderation_rationale(rationale: str) -> list[float]:
    client = get_openai_client()
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=rationale,
    )
    return response.data[0].embedding


def embed_multiple_rationales(rationales: list[str]) -> list[list[float]]:
    client = get_openai_client()
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=rationales,
    )
    return [item.embedding for item in response.data]


def build_rationale_embedding_record(rationale: str, case_id: str) -> dict:
    embedding = embed_moderation_rationale(rationale)
    return {
        "case_id": case_id,
        "rationale": rationale,
        "embedding": embedding,
        "model": EMBEDDING_MODEL,
        "dimension": len(embedding),
    }


def compute_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def find_similar_cases(
    query_rationale: str, case_embeddings: list[dict], top_k: int = 5
) -> list[dict]:
    query_embedding = embed_moderation_rationale(query_rationale)
    scored_cases = []
    for case in case_embeddings:
        similarity = compute_similarity(query_embedding, case["embedding"])
        scored_cases.append(
            {
                "case_id": case["case_id"],
                "rationale": case["rationale"],
                "similarity": similarity,
            }
        )
    scored_cases.sort(key=lambda x: x["similarity"], reverse=True)
    return scored_cases[:top_k]
