import os
from typing import List, Dict, Any
from anthropic import Anthropic


def embedding_job_summary(
    texts: List[str], embeddings: List[List[float]], job_metadata: Dict[str, Any]
) -> str:
    """Summarize embedding job results using Anthropic Claude."""
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Prepare summary data
    num_texts = len(texts)
    avg_text_length = sum(len(t) for t in texts) / num_texts if num_texts > 0 else 0
    embedding_dim = len(embeddings[0]) if embeddings else 0

    summary_prompt = f"""You are summarizing an embedding job. Here are the details:

Job Metadata:
- Model: {job_metadata.get("model", "Unknown")}
- Number of texts: {num_texts}
- Average text length: {avg_text_length:.1f} characters
- Embedding dimension: {embedding_dim}
- Provider: {job_metadata.get("provider", "Unknown")}

Sample texts (first 3):
{chr(10).join([f"- {t[:100]}..." if len(t) > 100 else f"- {t}" for t in texts[:3]])}

Please provide a concise summary of this embedding job, including:
1. Overall scope and scale
2. Any notable patterns in the text content
3. Potential use cases for these embeddings
4. Any quality considerations

Keep the summary professional and actionable."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[{"role": "user", "content": summary_prompt}],
    )

    return response.content[0].text
