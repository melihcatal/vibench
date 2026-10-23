from typing import List, Dict
from anthropic import Anthropic
import os


def summarize_embedding_job(
    job_id: str, embeddings: List[List[float]], texts: List[str]
) -> str:
    """
    Summarizes embedding job results using Anthropic's Claude model.

    Args:
        job_id: Unique identifier for the embedding job.
        embeddings: List of embedding vectors.
        texts: List of original texts that were embedded.

    Returns:
        Summary of the embedding job results.
    """
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    if not client.api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    prompt = f"Summarize the following embedding job results for job ID: {job_id}. "
    prompt += "Provide insights on the embedding distribution, potential use cases, and any anomalies.\n\n"
    prompt += "Texts and their embedding dimensions:\n"
    for i, (text, embedding) in enumerate(zip(texts, embeddings)):
        prompt += (
            f"Text {i + 1}: {text[:100]}... (Embedding dimension: {len(embedding)})\n"
        )

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text
