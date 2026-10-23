from typing import Any, Dict
from embeddings_client import get_anthropic_client


def embedding_job_summary(job_results: Dict[str, Any]) -> str:
    embeddings = job_results.get("embeddings", [])
    num_embeddings = len(embeddings)
    dimension = len(embeddings[0]) if embeddings else 0
    info = job_results.get("info", "No additional info")
    prompt = f"""Summarize the embedding job results concisely:

Number of embeddings generated: {num_embeddings}
Embedding dimension: {dimension}
Additional info: {info}

Provide key insights or observations about the job, such as scale, consistency, etc."""
    client = get_anthropic_client()
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    return message.content[0].text
