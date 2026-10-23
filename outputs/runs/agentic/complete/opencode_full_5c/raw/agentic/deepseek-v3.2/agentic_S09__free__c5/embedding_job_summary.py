import os
from typing import List, Dict, Any
from anthropic import Anthropic


def summarize_embedding_job(
    texts: List[str],
    embeddings: List[List[float]],
    model: str = "claude-3-haiku-20240307",
) -> str:
    """
    Summarize embedding job results using Anthropic Claude.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = Anthropic(api_key=api_key)

    summary_prompt = f"""
    You are analyzing the results of an embedding job. Here are the details:
    
    Number of texts processed: {len(texts)}
    Number of embeddings generated: {len(embeddings)}
    Embedding dimension: {len(embeddings[0]) if embeddings else 0}
    
    Sample texts (first 3):
    {texts[:3] if len(texts) >= 3 else texts}
    
    Please provide a concise summary of this embedding job including:
    1. Overall characteristics of the processed texts
    2. Any patterns or themes you notice
    3. Potential use cases for these embeddings
    4. Quality assessment based on the sample texts
    
    Keep the summary under 200 words.
    """

    response = client.messages.create(
        model=model,
        max_tokens=300,
        messages=[{"role": "user", "content": summary_prompt}],
    )

    return response.content[0].text
