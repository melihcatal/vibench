"""
Summarize embedding job results.

Provider: OpenAI Embeddings API
Provider SDK: openai
Provider Model: text-embedding-3-small
Provider Env: OPENAI_API_KEY
Provider Host: api.openai.com
"""

from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingResponse


def embedding_job_summary(
    texts: list[str],
    model: str = "text-embedding-3-small",
    dimensions: int = 1536,
) -> dict:
    """Embed a corpus of texts and produce a summary of the embedding job results.

    Returns a dict with statistics about the embedding job using OpenAI.

    Args:
        texts: List of text strings to embed.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        dimensions: Output embedding dimensions.

    Returns:
        Summary dict with job metadata and statistics.
    """
    client = EmbeddingsClient(model=model, dimensions=dimensions)

    # Batch embed all texts via the OpenAI embeddings API
    response_data = client.client.embeddings.create(
        model=model,
        input=texts,
        dimensions=dimensions,
    )
    usage_info = client.get_usage_info(response_data)

    ordered = sorted(response_data.data, key=lambda d: d.index)
    embeddings = [item.embedding for item in ordered]

    # Compute embedding statistics
    dim = len(embeddings[0]) if embeddings else 0
    mean_norms = []
    for emb in embeddings:
        norm = sum(x * x for x in emb) ** 0.5
        mean_norms.append(norm)

    avg_norm = sum(mean_norms) / len(mean_norms) if mean_norms else 0.0

    # Compute pairwise similarity sample (first 5 pairs max)
    pair_scores = []
    sample_size = min(len(embeddings), 5)
    for i in range(sample_size):
        for j in range(i + 1, sample_size):
            a, b = embeddings[i], embeddings[j]
            dot = sum(x * y for x, y in zip(a, b))
            na = sum(x * x for x in a) ** 0.5
            nb = sum(x * x for x in b) ** 0.5
            if na > 0 and nb > 0:
                pair_scores.append(dot / (na * nb))

    avg_similarity = sum(pair_scores) / len(pair_scores) if pair_scores else 0.0

    return {
        "provider": "openai",
        "model": model,
        "total_documents": len(texts),
        "embedding_dimensions": dim,
        "average_vector_norm": round(avg_norm, 6),
        "average_pairwise_similarity": round(avg_similarity, 6),
        "total_prompt_tokens": usage_info.get("prompt_tokens", 0),
        "total_tokens": usage_info.get("total_tokens", 0),
    }


if __name__ == "__main__":
    corpus = [
        "OpenAI provides state-of-the-art language models.",
        "Embedding models convert text into dense vector representations.",
        "Semantic search uses embeddings to find relevant documents.",
        "The text-embedding-3-small model is optimized for cost and speed.",
    ]
    summary = embedding_job_summary(corpus)
    for key, value in summary.items():
        print(f"{key}: {value}")
