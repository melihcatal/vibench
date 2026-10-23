from safety_client import get_openai_client, OPENAI_EMBEDDING_MODEL
from safety_models import EmbeddingResult


def embed_moderation_reason(reason_text):
    client = get_openai_client()
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=reason_text,
        encoding_format="float",
    )
    data = response.data[0]
    return EmbeddingResult(
        text=reason_text,
        embedding=data.embedding,
        model=response.model,
        usage_tokens=response.usage.total_tokens,
    )


def embed_moderation_reasons(reason_texts):
    client = get_openai_client()
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=reason_texts,
        encoding_format="float",
    )
    results = []
    for i, data in enumerate(response.data):
        results.append(
            EmbeddingResult(
                text=reason_texts[i],
                embedding=data.embedding,
                model=response.model,
                usage_tokens=response.usage.total_tokens,
            )
        )
    return results


def build_case_rationale(moderation_result):
    categories = moderation_result.categories.flagged_categories()
    scores = moderation_result.category_scores.to_dict()
    flagged_scores = {cat: scores.get(cat, 0.0) for cat in categories}
    rationale_parts = [f"Content was flagged for: {', '.join(categories)}."]
    for cat, score in flagged_scores.items():
        rationale_parts.append(f"  - {cat}: {score:.4f}")
    rationale_parts.append(f"Original text: {moderation_result.text[:500]}")
    return " ".join(rationale_parts)


def embed_case_for_retrieval(moderation_result):
    rationale = build_case_rationale(moderation_result)
    return embed_moderation_reason(rationale)


def cosine_similarity(vec_a, vec_b):
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimension")
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def find_similar_cases(query_embedding, case_embeddings, top_k=5):
    similarities = []
    for i, case_emb in enumerate(case_embeddings):
        sim = cosine_similarity(query_embedding, case_emb)
        similarities.append((i, sim))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]
