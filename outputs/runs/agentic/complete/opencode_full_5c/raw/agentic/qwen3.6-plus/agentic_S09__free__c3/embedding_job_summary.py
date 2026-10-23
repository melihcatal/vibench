from embeddings_models import EmbeddingJobSummary, BatchEmbeddingResponse


def embedding_job_summary(batch_response, failed_indices=None):
    if failed_indices is None:
        failed_indices = []
    successful = len(batch_response) - len(failed_indices)
    failed = len(failed_indices)
    total_texts = successful + failed
    avg_tokens = batch_response.usage.get("prompt_tokens", 0) / max(total_texts, 1)
    total_tokens = batch_response.usage.get("total_tokens", 0)
    return EmbeddingJobSummary(
        total_texts=total_texts,
        successful=successful,
        failed=failed,
        avg_tokens=avg_tokens,
        model=batch_response.model,
        total_tokens=total_tokens,
    )


def format_summary(summary):
    lines = [
        f"Embedding Job Summary",
        f"  Model: {summary.model}",
        f"  Total texts: {summary.total_texts}",
        f"  Successful: {summary.successful}",
        f"  Failed: {summary.failed}",
        f"  Avg tokens per text: {summary.avg_tokens:.1f}",
        f"  Total tokens: {summary.total_tokens}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    from embed_batch import embed_batch

    texts = [
        "The quick brown fox jumps over the lazy dog",
        "Machine learning is a subset of artificial intelligence",
        "Python is a popular programming language",
    ]
    result = embed_batch(texts)
    summary = embedding_job_summary(result)
    print(format_summary(summary))
