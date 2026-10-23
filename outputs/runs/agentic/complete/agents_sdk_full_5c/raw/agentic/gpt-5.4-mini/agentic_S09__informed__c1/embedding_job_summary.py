from __future__ import annotations

from openai import OpenAI

from embeddings_client import get_openai_client

SUMMARY_MODEL = "gpt-4o-mini"


def summarize_embedding_job(job_name: str, completed: int, failed: int) -> str:
    client: OpenAI = get_openai_client()
    prompt = (
        f"Summarize the embedding job named {job_name!r}. "
        f"Completed: {completed}. Failed: {failed}. "
        "Keep it concise and operational."
    )
    response = client.chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": "You summarize embedding pipeline outcomes."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""
