from __future__ import annotations

from collections.abc import Sequence

from openai import OpenAI


def embedding_job_summary(
    job_name: str, texts_processed: int, model: str, failures: Sequence[str]
) -> str:
    client = OpenAI(api_key=__import__("os").environ["OPENAI_API_KEY"])
    prompt = {
        "job_name": job_name,
        "texts_processed": texts_processed,
        "embedding_model": model,
        "failures": list(failures),
    }
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize embedding batch outcomes for operators.",
            },
            {"role": "user", "content": str(prompt)},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
