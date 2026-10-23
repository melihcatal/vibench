from typing import List, Dict, Optional
from openai import OpenAI
from embeddings_client import build_embeddings_client, load_config_from_env
from embeddings_models import EmbeddingJobSummary


def summarize_embedding_job(
    texts: List[str],
    model: str = "text-embedding-3-small",
    dimensions: int = None,
) -> EmbeddingJobSummary:
    config = load_config_from_env()
    client: OpenAI = build_embeddings_client(api_key=config["api_key"])
    total_tokens = 0
    success_count = 0
    failed_count = 0
    embedding_dimensions = 0
    for text in texts:
        try:
            response = client.embeddings.create(
                model=model,
                input=text,
                encoding_format="float",
                dimensions=dimensions,
            )
            total_tokens += response.usage.prompt_tokens
            if response.data:
                embedding_dimensions = len(response.data[0].embedding)
                success_count += 1
        except Exception:
            failed_count += 1
    total_texts = len(texts)
    avg_tokens = total_tokens / total_texts if total_texts > 0 else 0.0
    return EmbeddingJobSummary(
        total_texts=total_texts,
        total_tokens=total_tokens,
        model=model,
        dimensions=embedding_dimensions,
        average_token_length=avg_tokens,
        success_count=success_count,
        failed_count=failed_count,
    )


def format_job_summary(summary: EmbeddingJobSummary) -> str:
    lines = [
        f"Embedding Job Summary",
        f"  Model: {summary.model}",
        f"  Total texts processed: {summary.total_texts}",
        f"  Successful: {summary.success_count}",
        f"  Failed: {summary.failed_count}",
        f"  Total tokens used: {summary.total_tokens}",
        f"  Average tokens per text: {summary.average_token_length:.1f}",
        f"  Embedding dimensions: {summary.dimensions}",
    ]
    return "\n".join(lines)


def generate_batch_summary(
    texts: List[str],
    model: str = "text-embedding-3-small",
) -> Dict:
    config = load_config_from_env()
    client: OpenAI = build_embeddings_client(api_key=config["api_key"])
    response = client.embeddings.create(
        model=model,
        input=texts,
        encoding_format="float",
    )
    total_tokens = response.usage.prompt_tokens
    embedding_dim = len(response.data[0].embedding) if response.data else 0
    return {
        "model": response.model,
        "total_texts": len(texts),
        "total_tokens": total_tokens,
        "average_tokens_per_text": total_tokens / len(texts) if texts else 0,
        "embedding_dimensions": embedding_dim,
        "success_count": len(response.data),
        "failed_count": 0,
    }


if __name__ == "__main__":
    texts = [
        "Natural language processing enables computers to understand human language",
        "Computer vision allows machines to interpret visual information",
        "Reinforcement learning trains agents through rewards and penalties",
    ]
    summary = summarize_embedding_job(texts)
    print(format_job_summary(summary))
