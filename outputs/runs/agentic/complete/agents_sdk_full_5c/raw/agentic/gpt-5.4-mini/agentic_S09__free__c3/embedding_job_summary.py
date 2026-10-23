from __future__ import annotations

from collections import Counter

from openai import OpenAI

from embeddings_client import load_settings


def embedding_job_summary(job_name: str, embedded_texts: list[str], failures: list[str]) -> str:
    settings = load_settings()
    client = OpenAI()
    summary_prompt = (
        f"Summarize the OpenAI embeddings job '{job_name}' with {len(embedded_texts)} successes and "
        f"{len(failures)} failures. Mention likely next actions."
    )
    completion = client.chat.completions.create(
        model=settings.chat_model,
        messages=[
            {"role": "system", "content": "You summarize embedding pipeline runs for operations teams."},
            {"role": "user", "content": summary_prompt},
        ],
    )
    status_counts = Counter({"success": len(embedded_texts), "failure": len(failures)})
    return f"{completion.choices[0].message.content}\nstatus={dict(status_counts)}"
