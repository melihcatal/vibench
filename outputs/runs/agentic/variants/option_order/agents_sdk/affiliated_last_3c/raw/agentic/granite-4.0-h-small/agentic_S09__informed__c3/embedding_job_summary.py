import json

def embedding_job_summary(results: list[dict]) -> str:
    """Summarize a batch embedding job's results.

    Args:
        results (list[dict]): Raw response objects from the embedding API.

    Returns:
        str: Human‑readable summary including number of successes, errors, and sample vectors.
    """
    total = len(results)
    successes = sum(1 for r in results if 'error' not in r)
    failures = total - successes
    sample = next((r['data'][0]['embedding'] for r in results if 'error' not in r), [])
    summary = (
        f"Embedding job summary:\n"
        f"  Total requests: {total}\n"
        f"  Successful embeddings: {successes}\n"
        f"  Failed requests: {failures}\n"
        f"  Sample embedding length: {len(sample)} dimensions\n"
    )
    return summary
