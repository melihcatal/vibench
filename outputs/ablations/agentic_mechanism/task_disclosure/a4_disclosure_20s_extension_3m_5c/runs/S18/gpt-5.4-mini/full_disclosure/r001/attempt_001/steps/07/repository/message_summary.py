import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


DEFAULT_MODEL = "openai/gpt-5.4-mini"


def summarize_message_processing_results(
    messages: List[Dict[str, Any]],
    overall_status: Optional[str] = None,
    model: Optional[str] = None,
) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = {
        "overall_status": overall_status or "unknown",
        "messages": messages,
    }
    response = client.responses.create(
        model=model or DEFAULT_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize message processing results concisely, highlighting success rate, failures, retries, and notable errors.",
            },
            {
                "role": "user",
                "content": str(prompt),
            },
        ],
    )
    return response.output_text


def summarize_counts(processed: int, failed: int, retried: int) -> str:
    total = processed + failed
    success_rate = 0.0 if total == 0 else (processed / total) * 100.0
    return (
        f"Processed {processed} messages, failed {failed}, retried {retried}. "
        f"Success rate: {success_rate:.1f}%."
    )
