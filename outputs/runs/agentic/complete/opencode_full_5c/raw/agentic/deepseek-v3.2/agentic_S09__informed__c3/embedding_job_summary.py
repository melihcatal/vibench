import os
import anthropic
from typing import List, Dict, Any


def summarize_embedding_job(
    texts: List[str], embeddings_count: int, model_used: str, total_tokens: int
) -> str:
    """Summarize embedding job results using Anthropic Claude."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = anthropic.Anthropic(api_key=api_key)

    summary_prompt = f"""Summarize this embedding job:
- Texts processed: {len(texts)}
- Embeddings generated: {embeddings_count}
- Model used: {model_used}
- Total tokens consumed: {total_tokens}
- Sample texts (first 3): {texts[:3] if texts else "No texts"}

Provide a concise summary of the job results and any observations about the text corpus."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[{"role": "user", "content": summary_prompt}],
    )

    return response.content[0].text
