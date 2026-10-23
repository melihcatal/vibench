import os
from openai import OpenAI
from embeddings_client import get_openai_client, DEFAULT_EMBEDDING_MODEL


def embedding_job_summary(
    texts: list[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> dict:
    client = get_openai_client()
    response = client.embeddings.create(
        input=texts,
        model=model,
    )
    sorted_data = sorted(response.data, key=lambda d: d.index)
    embeddings = [item.embedding for item in sorted_data]
    dimension = len(embeddings[0]) if embeddings else 0
    total_tokens = response.usage.total_tokens if response.usage else 0
    prompt_tokens = response.usage.prompt_tokens if response.usage else 0
    return {
        "job_id": response.id if hasattr(response, "id") else None,
        "model": model,
        "num_texts": len(texts),
        "embedding_dimension": dimension,
        "total_tokens_consumed": total_tokens,
        "prompt_tokens": prompt_tokens,
        "average_tokens_per_text": total_tokens / len(texts) if texts else 0,
        "embeddings_count": len(embeddings),
        "status": "completed",
    }
