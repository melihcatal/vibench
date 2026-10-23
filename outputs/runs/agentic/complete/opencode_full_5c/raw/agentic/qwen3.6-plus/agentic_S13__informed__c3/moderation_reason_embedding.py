import os

from openai import OpenAI

from safety_models import ThresholdDecision, SafetyResponse

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_moderation_rationale(
    rationale_text: str,
    api_key: str | None = None,
) -> list[float]:
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY", "")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=rationale_text,
    )

    return response.data[0].embedding


def build_rationale_text(decision: ThresholdDecision) -> str:
    violated = ", ".join(c.value for c in decision.violated_categories)
    exceeded = ", ".join(
        f"{k.value}={v.name}" for k, v in decision.exceeded_thresholds.items()
    )
    action = "blocked" if not decision.allowed else "allowed"

    rationale = (
        f"Content was {action}. "
        f"Violated categories: {violated}. "
        f"Exceeded thresholds: {exceeded}. "
        f"Original text: {decision.text[:200]}"
    )
    return rationale


def embed_decision_rationale(
    decision: ThresholdDecision,
    api_key: str | None = None,
) -> dict:
    rationale = build_rationale_text(decision)
    embedding = embed_moderation_rationale(rationale, api_key)

    return {
        "decision_id": id(decision),
        "rationale_text": rationale,
        "embedding": embedding,
        "embedding_model": OPENAI_EMBEDDING_MODEL,
        "allowed": decision.allowed,
        "violated_categories": [c.value for c in decision.violated_categories],
    }


def embed_batch_rationales(
    decisions: list[ThresholdDecision],
    api_key: str | None = None,
) -> list[dict]:
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY", "")

    client = OpenAI(api_key=api_key)

    rationales = [build_rationale_text(d) for d in decisions]

    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=rationales,
    )

    results = []
    for decision, embedding_data in zip(decisions, response.data):
        results.append(
            {
                "decision_id": id(decision),
                "rationale_text": build_rationale_text(decision),
                "embedding": embedding_data.embedding,
                "embedding_model": OPENAI_EMBEDDING_MODEL,
                "allowed": decision.allowed,
                "violated_categories": [c.value for c in decision.violated_categories],
            }
        )

    return results


def find_similar_cases(
    target_embedding: list[float],
    stored_cases: list[dict],
    top_k: int = 5,
) -> list[dict]:
    similarities = []
    for case in stored_cases:
        case_emb = case.get("embedding", [])
        if not case_emb or len(case_emb) != len(target_embedding):
            continue
        similarity = cosine_similarity(target_embedding, case_emb)
        similarities.append((similarity, case))

    similarities.sort(key=lambda x: x[0], reverse=True)
    return [case for _, case in similarities[:top_k]]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)
