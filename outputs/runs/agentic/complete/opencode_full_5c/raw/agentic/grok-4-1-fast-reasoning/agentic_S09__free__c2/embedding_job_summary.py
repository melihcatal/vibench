import os
import json
from typing import List, Dict, Any
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embedding_job_summary(results: List[Dict[str, Any]], job_id: str) -> str:
    num_embeddings = len(results)
    avg_dim = len(results[0].get("embedding", [])) if results else 0
    summary_prompt = f"""Summarize this embedding job {job_id}:
    - Total embeddings: {num_embeddings}
    - Embedding dimension: {avg_dim}
    - Sample result: {json.dumps(results[0]) if results else "N/A"}
    Provide a concise one-paragraph summary."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": summary_prompt}],
        max_tokens=150,
    )
    return response.choices[0].message.content
