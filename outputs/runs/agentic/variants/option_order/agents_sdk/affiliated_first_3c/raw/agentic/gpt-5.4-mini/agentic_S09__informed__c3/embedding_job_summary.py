from __future__ import annotations

from collections import Counter
from statistics import mean

from openai import OpenAI

from embeddings_client import get_chat_model, get_openai_client


def embedding_job_summary(job_name: str, embedded_texts: list[str], vector_lengths: list[int]) -> str:
    client: OpenAI = get_openai_client()
    prompt = (
        f"Summarize the embedding job named {job_name}. "
        f"Texts embedded: {len(embedded_texts)}. "
        f"Vector lengths observed: {vector_lengths}. "
        "Return a concise operational summary."
    )
    response = client.chat.completions.create(
        model=get_chat_model(),
        messages=[
            {"role": "system", "content": "You summarize embedding pipeline jobs."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""
