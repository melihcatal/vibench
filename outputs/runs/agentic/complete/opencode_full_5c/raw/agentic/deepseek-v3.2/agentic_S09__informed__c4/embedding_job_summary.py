import os
from typing import List, Dict, Any
import anthropic
from embeddings_models import EmbeddingResponse


def summarize_embedding_job(results: EmbeddingResponse, query: str = None) -> str:
    """Summarize embedding job results using Anthropic Claude."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = anthropic.Anthropic(api_key=api_key)

    num_embeddings = len(results.embeddings)
    embedding_dim = len(results.embeddings[0]) if num_embeddings > 0 else 0
    prompt_tokens = results.usage.get("prompt_tokens", 0)
    total_tokens = results.usage.get("total_tokens", 0)

    summary_prompt = f"""Summarize this embedding job:
- Model: {results.model}
- Number of embeddings generated: {num_embeddings}
- Embedding dimension: {embedding_dim}
- Token usage: {prompt_tokens} prompt tokens, {total_tokens} total tokens
"""

    if query:
        summary_prompt += f"- Query context: {query}\n"

    summary_prompt += "Provide a concise summary suitable for logging and monitoring."

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=200,
        messages=[{"role": "user", "content": summary_prompt}],
    )

    return message.content[0].text
