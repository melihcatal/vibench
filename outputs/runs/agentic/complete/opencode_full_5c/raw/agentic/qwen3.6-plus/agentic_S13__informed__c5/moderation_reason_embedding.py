import os
from openai import OpenAI
from safety_models import ModerationResponse


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return OpenAI(api_key=api_key)


def build_moderation_rationale(moderation_result: ModerationResponse) -> str:
    violations = moderation_result.violating_categories
    scores_text = ", ".join(
        f"{s.category}={s.score:.3f}"
        for s in sorted(moderation_result.scores, key=lambda x: x.score, reverse=True)
    )

    rationale = (
        f"Moderation decision for text: '{moderation_result.text[:200]}'. "
        f"Overall violation: {moderation_result.overall_violation}. "
        f"Violating categories: {', '.join(violations) if violations else 'none'}. "
        f"All scores: {scores_text}."
    )

    return rationale


def embed_moderation_reason(
    moderation_result: ModerationResponse,
    model: str = "text-embedding-3-small",
    client: OpenAI | None = None,
) -> list[float]:
    if client is None:
        client = get_openai_client()

    rationale = build_moderation_rationale(moderation_result)

    response = client.embeddings.create(
        model=model,
        input=rationale,
        encoding_format="float",
    )

    return response.data[0].embedding


def embed_moderation_reasons_batch(
    moderation_results: list[ModerationResponse],
    model: str = "text-embedding-3-small",
    client: OpenAI | None = None,
) -> list[list[float]]:
    if client is None:
        client = get_openai_client()

    rationales = [build_moderation_rationale(r) for r in moderation_results]

    response = client.embeddings.create(
        model=model,
        input=rationales,
        encoding_format="float",
    )

    return [item.embedding for item in response.data]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = sum(x * x for x in a) ** 0.5
    mag_b = sum(x * x for x in b) ** 0.5
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def find_similar_cases(
    target_embedding: list[float],
    case_embeddings: list[tuple[str, list[float]]],
    top_k: int = 5,
) -> list[tuple[str, float]]:
    similarities = [
        (case_id, cosine_similarity(target_embedding, emb))
        for case_id, emb in case_embeddings
    ]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]


if __name__ == "__main__":
    from moderate_text import moderate_text

    input_text = "This is a test message for moderation."
    result = moderate_text(input_text)
    embedding = embed_moderation_reason(result)
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
