from __future__ import annotations

from messaging_client import get_openai_client
from messaging_models import ProcessingSummary


def summarize_message_processing(results: list[dict]) -> ProcessingSummary:
    client = get_openai_client()
    success_count = sum(1 for item in results if item.get("status") == "success")
    failure_count = len(results) - success_count
    completion = client.responses.create(
        model="gpt-5.4",
        input=[
            {
                "role": "system",
                "content": "Summarize message processing outcomes concisely for operators.",
            },
            {
                "role": "user",
                "content": str(results),
            },
        ],
    )
    return ProcessingSummary(
        provider="openai",
        total_messages=len(results),
        success_count=success_count,
        failure_count=failure_count,
        summary_text=completion.output_text,
    )
