import os
from typing import List
from openai import OpenAI

def embedding_job_summary(embeddings: List[list[float]], texts: List[str]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    num_emb = len(embeddings)
    dim = len(embeddings[0]) if embeddings else 0
    sample_texts = texts[:3] if texts else []
    prompt = f"""Summarize this embedding job:
- Number of embeddings generated: {num_emb}
- Embedding dimension: {dim}
- Sample texts: {sample_texts}
Provide a concise summary."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
