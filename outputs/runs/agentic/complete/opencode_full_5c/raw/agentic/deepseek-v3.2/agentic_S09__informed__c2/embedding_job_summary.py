import os
from typing import List, Dict, Any
from anthropic import Anthropic


def summarize_embedding_job(
    results: List[Dict[str, Any]], model: str = "claude-3-5-sonnet-20241022"
) -> str:
    """
    Summarize embedding job results using Anthropic Claude.

    Args:
        results: List of embedding job results with keys: text, embedding_length, processing_time, success
        model: Anthropic model identifier

    Returns:
        str: Summary of embedding job
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = Anthropic(api_key=api_key)

    # Prepare summary data
    total_texts = len(results)
    successful = sum(1 for r in results if r.get("success", False))
    failed = total_texts - successful
    total_processing_time = sum(r.get("processing_time", 0) for r in results)
    avg_processing_time = total_processing_time / total_texts if total_texts > 0 else 0

    # Create prompt
    prompt = f"""Summarize the embedding job results:

Total texts processed: {total_texts}
Successful embeddings: {successful}
Failed embeddings: {failed}
Total processing time: {total_processing_time:.2f} seconds
Average processing time per text: {avg_processing_time:.2f} seconds

Provide a concise summary highlighting key metrics and any patterns observed in the failures (if any)."""

    response = client.messages.create(
        model=model, max_tokens=500, messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text
