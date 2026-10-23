import math
from embeddings_client import create_embeddings_client, handle_embedding_error
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embedding_job_summary(texts, model=None, client=None, api_key=None):
    if not texts:
        raise ValueError("texts list must not be empty")

    if client is None:
        client, model = create_embeddings_client(model=model, api_key=api_key)

    if model is None:
        model = "text-embedding-3-small"

    request = EmbeddingRequest(
        texts=texts,
        model=model,
    )

    try:
        response = client.embeddings.create(**request.to_payload())
        result = EmbeddingResponse.from_openai_response(response)
    except Exception as exc:
        handle_embedding_error(exc)

    embeddings = result.embeddings
    dimension = result.embedding_dimension()

    token_counts = []
    text_lengths = []
    for text in texts:
        token_counts.append(len(text.split()))
        text_lengths.append(len(text))

    avg_token_count = sum(token_counts) / len(token_counts) if token_counts else 0
    avg_text_length = sum(text_lengths) / len(text_lengths) if text_lengths else 0

    centroid = [0.0] * dimension
    for emb in embeddings:
        for i, val in enumerate(emb):
            centroid[i] += val
    centroid = [c / len(embeddings) for c in centroid]

    distances_to_centroid = []
    for emb in embeddings:
        dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(emb, centroid)))
        distances_to_centroid.append(dist)

    avg_distance = sum(distances_to_centroid) / len(distances_to_centroid)
    max_distance = max(distances_to_centroid)
    min_distance = min(distances_to_centroid)

    pairwise_similarities = []
    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            dot = sum(a * b for a, b in zip(embeddings[i], embeddings[j]))
            norm_i = math.sqrt(sum(x * x for x in embeddings[i]))
            norm_j = math.sqrt(sum(x * x for x in embeddings[j]))
            if norm_i > 0 and norm_j > 0:
                pairwise_similarities.append(dot / (norm_i * norm_j))

    avg_pairwise_similarity = (
        sum(pairwise_similarities) / len(pairwise_similarities)
        if pairwise_similarities
        else 0.0
    )

    return {
        "model": model,
        "total_texts": len(texts),
        "embedding_dimension": dimension,
        "total_prompt_tokens": result.usage.get("prompt_tokens", 0),
        "total_tokens": result.usage.get("total_tokens", 0),
        "avg_tokens_per_text": avg_token_count,
        "avg_text_length_chars": avg_text_length,
        "avg_distance_to_centroid": avg_distance,
        "max_distance_to_centroid": max_distance,
        "min_distance_to_centroid": min_distance,
        "avg_pairwise_cosine_similarity": avg_pairwise_similarity,
        "embedding_spread": max_distance - min_distance,
    }
