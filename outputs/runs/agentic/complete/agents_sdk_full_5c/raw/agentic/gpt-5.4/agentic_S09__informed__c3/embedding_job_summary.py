from __future__ import annotations

from openai import OpenAI



def summarize_embedding_job_results(
    total_items: int,
    succeeded_items: int,
    failed_items: int,
    model: str,
    sample_errors: list[str] | None = None,
    sample_scores: list[float] | None = None,
    summary_model: str = "gpt-4o-mini",
) -> str:
    client = OpenAI()
    prompt = {
        "total_items": total_items,
        "succeeded_items": succeeded_items,
        "failed_items": failed_items,
        "embedding_model": model,
        "sample_errors": sample_errors or [],
        "sample_scores": sample_scores or [],
    }
    response = client.chat.completions.create(
        model=summary_model,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "You are an operations analyst summarizing OpenAI embedding batch outcomes for engineers.",
            },
            {
                "role": "user",
                "content": f"Summarize this embedding job result in 4 concise bullets and include risks if any: {prompt}",
            },
        ],
    )
    return response.choices[0].message.content or ""
