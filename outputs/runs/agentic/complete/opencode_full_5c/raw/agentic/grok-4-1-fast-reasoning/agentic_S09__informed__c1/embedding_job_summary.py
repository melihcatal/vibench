import os
import json
from openai import OpenAI
from typing import List, Dict, Any


def embedding_job_summary(job_results: List[Dict[str, Any]]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = OpenAI(api_key=api_key)

    num_embeddings = len(job_results)
    total_dims = sum(len(r.get("embedding", [])) for r in job_results)
    avg_dims = total_dims / num_embeddings if num_embeddings else 0

    prompt = f"""Summarize the embedding job results in 1-2 sentences:
- Processed {num_embeddings} documents
- Average embedding dimension: {avg_dims:.0f}
- Model used: text-embedding-3-small"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
    )
    return response.choices[0].message.content.strip()
