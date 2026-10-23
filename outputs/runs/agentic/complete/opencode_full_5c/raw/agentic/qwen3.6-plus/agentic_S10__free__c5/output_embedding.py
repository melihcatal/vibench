import math

from model_client import HostedLLMClient
from model_models import EmbeddingRequest, EmbeddingResponse, ModelConfig


def generate_embeddings(
    texts: str | list[str],
    model: str = "text-embedding-3-small",
    dimensions: int | None = None,
    config: ModelConfig | None = None,
) -> EmbeddingResponse:
    client = HostedLLMClient(config=config)
    request = EmbeddingRequest(
        input=texts,
        model=model,
        dimensions=dimensions,
    )
    return client.create_embeddings(request)


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def find_most_similar(
    query: str,
    candidates: list[str],
    model: str = "text-embedding-3-small",
    config: ModelConfig | None = None,
) -> list[tuple[int, float]]:
    all_texts = [query] + candidates
    response = generate_embeddings(all_texts, model=model, config=config)
    query_vec = response.embeddings[0]
    candidate_vecs = response.embeddings[1:]
    scores = []
    for i, vec in enumerate(candidate_vecs):
        sim = cosine_similarity(query_vec, vec)
        scores.append((i, sim))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


def cluster_by_similarity(
    texts: list[str],
    model: str = "text-embedding-3-small",
    similarity_threshold: float = 0.8,
    config: ModelConfig | None = None,
) -> list[list[int]]:
    response = generate_embeddings(texts, model=model, config=config)
    vectors = response.embeddings
    clusters: list[list[int]] = []
    assigned: set[int] = set()
    for i in range(len(vectors)):
        if i in assigned:
            continue
        cluster = [i]
        assigned.add(i)
        for j in range(i + 1, len(vectors)):
            if j in assigned:
                continue
            sim = cosine_similarity(vectors[i], vectors[j])
            if sim >= similarity_threshold:
                cluster.append(j)
                assigned.add(j)
        clusters.append(cluster)
    return clusters


if __name__ == "__main__":
    texts = [
        "Machine learning models process data to find patterns.",
        "Neural networks are inspired by biological brains.",
        "The weather is sunny and warm today.",
        "Deep learning uses multiple layers of neurons.",
    ]
    response = generate_embeddings(texts)
    print(f"Generated {len(response.embeddings)} embeddings using {response.model}")
    print(f"Embedding dimension: {len(response.embeddings[0])}")
    print(f"Total tokens: {response.total_tokens}")
