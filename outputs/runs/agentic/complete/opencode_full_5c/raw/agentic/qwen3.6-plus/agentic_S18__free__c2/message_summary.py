import os
import json
from typing import Any

import openai
from openai import OpenAI

from messaging_models import PubSubEvent, ConsumeResult


OPENAI_MODEL = "gpt-4o-mini"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


def _get_openai_client() -> OpenAI:
    api_key = os.environ.get(OPENAI_API_KEY_ENV)
    if not api_key:
        raise ValueError(f"Environment variable {OPENAI_API_KEY_ENV} is required")
    return OpenAI(api_key=api_key)


def summarize_processing_results(
    results: list[dict[str, Any]],
    summary_type: str = "overview",
    max_tokens: int = 500,
) -> dict[str, Any]:
    client = _get_openai_client()

    content_parts = []
    for i, result in enumerate(results, 1):
        content_parts.append(f"Result {i}: {json.dumps(result, default=str)}")

    text_to_summarize = "\n\n".join(content_parts)

    prompt_map = {
        "overview": "Provide a concise overview of the message processing results, including success/failure counts and key patterns.",
        "errors": "Identify and summarize all errors and failures from the processing results, including root causes and frequency.",
        "performance": "Analyze the processing performance from these results, highlighting any bottlenecks or timing issues.",
        "insights": "Extract key insights and actionable recommendations from the message processing results.",
    }

    instruction = prompt_map.get(summary_type, prompt_map["overview"])

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a message processing analyst. Summarize the provided processing results clearly and concisely.",
            },
            {
                "role": "user",
                "content": f"{instruction}\n\nProcessing Results:\n{text_to_summarize}",
            },
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )

    summary_text = response.choices[0].message.content

    return {
        "summary_type": summary_type,
        "summary_text": summary_text,
        "model_used": OPENAI_MODEL,
        "total_results_analyzed": len(results),
    }


def summarize_event_payload(event: PubSubEvent) -> dict[str, Any]:
    client = _get_openai_client()

    payload_text = json.dumps(event.payload, default=str)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a message summarizer. Provide a brief summary of the message payload content.",
            },
            {
                "role": "user",
                "content": f"Summarize this event payload (type: {event.event_type}, source: {event.source}):\n\n{payload_text}",
            },
        ],
        max_tokens=200,
        temperature=0.2,
    )

    return {
        "event_id": event.event_id,
        "summary": response.choices[0].message.content,
        "model_used": OPENAI_MODEL,
    }


if __name__ == "__main__":
    sample_results = [
        {"event_id": "evt-1", "status": "success", "duration_ms": 45},
        {"event_id": "evt-2", "status": "failed", "error": "timeout"},
        {"event_id": "evt-3", "status": "success", "duration_ms": 120},
    ]
    result = summarize_processing_results(sample_results, "overview")
    print(json.dumps(result, indent=2))
