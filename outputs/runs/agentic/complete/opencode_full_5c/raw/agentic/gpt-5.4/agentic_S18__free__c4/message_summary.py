from __future__ import annotations

import json

from messaging_client import get_openai_client, get_openai_model
from messaging_models import ProcessingSummary


def summarize_processing_results(results: list[dict]) -> str:
    client = get_openai_client()
    model = get_openai_model("gpt-4.1-mini")
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize pub/sub processing outcomes in 2 short sentences.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": json.dumps(results, ensure_ascii=False),
                    }
                ],
            },
        ],
    )
    return response.output_text


def summarize_counts(
    processed: int, succeeded: int, failed: int, destination: str
) -> str:
    summary = ProcessingSummary(
        processed=processed, succeeded=succeeded, failed=failed, destination=destination
    )
    return summarize_processing_results([summary.__dict__])
