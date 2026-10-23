import openai

EMBEDDING_MODEL = "text-embedding-3-small"


def _build_rationale_text(result: dict) -> str:
    parts = []
    if result.get("text"):
        parts.append(f"Text: {result['text']}")
    if result.get("categories"):
        cat_parts = []
        for cat in result["categories"]:
            cat_parts.append(
                f"{cat.get('category', 'unknown')}={cat.get('severity', 'unknown')}"
            )
        parts.append(f"Categories: {', '.join(cat_parts)}")
    if result.get("reason"):
        parts.append(f"Reason: {result['reason']}")
    return " | ".join(parts)


def moderation_reason_embedding(
    moderation_result: dict,
    api_key: str | None = None,
    model: str = EMBEDDING_MODEL,
) -> dict:
    client = openai.OpenAI(api_key=api_key)
    rationale = _build_rationale_text(moderation_result)
    response = client.embeddings.create(
        model=model,
        input=rationale,
    )
    embedding = response.data[0].embedding
    return {
        "rationale_text": rationale,
        "embedding": embedding,
        "model": model,
        "embedding_dimension": len(embedding),
        "usage_tokens": response.usage.total_tokens,
    }


def embed_moderation_rationales(
    results: list[dict],
    api_key: str | None = None,
    model: str = EMBEDDING_MODEL,
) -> list[dict]:
    client = openai.OpenAI(api_key=api_key)
    rationales = [_build_rationale_text(r) for r in results]
    response = client.embeddings.create(
        model=model,
        input=rationales,
    )
    output = []
    for i, data in enumerate(response.data):
        output.append(
            {
                "index": i,
                "rationale_text": rationales[i],
                "embedding": data.embedding,
                "model": model,
                "embedding_dimension": len(data.embedding),
            }
        )
    return output
