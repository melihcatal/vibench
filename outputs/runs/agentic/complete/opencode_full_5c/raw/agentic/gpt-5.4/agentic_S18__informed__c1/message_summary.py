from __future__ import annotations

from openai import OpenAI

from messaging_models import ProcessingResult, json_dumps


def summarize_message_processing(results: list[ProcessingResult | dict]) -> dict:
    client = OpenAI()
    payload = [
        result.__dict__ if isinstance(result, ProcessingResult) else result
        for result in results
    ]
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize message processing results as compact JSON with keys summary, success_count, failure_count, and recommendations.",
            },
            {
                "role": "user",
                "content": json_dumps({"results": payload}),
            },
        ],
    )
    return {
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "summary": response.output_text,
    }
