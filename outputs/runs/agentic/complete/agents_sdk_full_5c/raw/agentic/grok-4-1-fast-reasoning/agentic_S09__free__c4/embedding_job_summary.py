from embeddings_client import get_client
from typing import Any, List

def embedding_job_summary(job_results: List[dict]) -> str:
    client = get_client()
    prompt = f"""Summarize the embedding job results in a concise paragraph.
Include key stats like number of texts embedded, model used if available, and any notable patterns.
Results: {job_results}"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content