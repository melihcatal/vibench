from __future__ import annotations

from collections.abc import Sequence

from openai import OpenAI


def embedding_job_summary(
    job_results: Sequence[dict], model: str = "gpt-4o-mini"
) -> dict:
    client = OpenAI(
        api_key=__import__("os").getenv("OPENAI_API_KEY"),
        base_url=__import__("os").getenv(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        ),
    )
    completion = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize embedding job outcomes with counts, anomalies, and next actions.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": str(list(job_results))}],
            },
        ],
    )
    return {
        "provider": "openai",
        "model": model,
        "summary": completion.output_text,
    }
