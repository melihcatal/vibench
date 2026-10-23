from typing import Dict, Any
from embeddings_client import get_client


def embedding_job_summary(job_results: Dict[str, Any]) -> str:
    client = get_client()
    prompt = f"""Provide a concise 1-2 sentence summary of this embedding job:

{job_results}"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
    )
    return response.choices[0].message.content.strip()
