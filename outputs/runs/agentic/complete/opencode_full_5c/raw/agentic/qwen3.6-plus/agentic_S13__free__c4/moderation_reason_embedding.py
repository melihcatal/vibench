from safety_client import call_embedding, OPENAI_EMBEDDING_MODEL
from safety_models import EmbeddingResult


def embed_moderation_reason(reason_text, model=None):
    response = call_embedding(reason_text, model=model or OPENAI_EMBEDDING_MODEL)
    data = response.data[0]
    return EmbeddingResult(
        text=reason_text,
        embedding=data.embedding,
        model=response.model,
        usage={
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    )


def embed_moderation_reasons(reason_texts, model=None):
    response = call_embedding(reason_texts, model=model or OPENAI_EMBEDDING_MODEL)
    results = []
    for item, original_text in zip(response.data, reason_texts):
        results.append(
            EmbeddingResult(
                text=original_text,
                embedding=item.embedding,
                model=response.model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
            )
        )
    return results


def compute_embedding_similarity(embedding_a, embedding_b):
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embeddings must have the same dimension")
    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def find_similar_cases(query_reason, case_embeddings, top_k=5):
    query_result = embed_moderation_reason(query_reason)
    query_embedding = query_result.embedding

    similarities = []
    for case in case_embeddings:
        sim = compute_embedding_similarity(query_embedding, case["embedding"])
        similarities.append(
            {"case_id": case["case_id"], "similarity": sim, "reason": case["reason"]}
        )

    similarities.sort(key=lambda x: x["similarity"], reverse=True)
    return similarities[:top_k]
