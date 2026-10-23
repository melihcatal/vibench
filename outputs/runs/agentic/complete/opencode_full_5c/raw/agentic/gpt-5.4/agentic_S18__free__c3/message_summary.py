from __future__ import annotations

from typing import Any, Dict, Iterable

from messaging_client import MODERATE_API_BASE, openai_headers, post_json
from messaging_models import ProcessingSummary


def message_summary(results: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    items = list(results)
    summary = ProcessingSummary(
        processed=len(items),
        succeeded=sum(1 for item in items if item.get("status") == "succeeded"),
        failed=sum(1 for item in items if item.get("status") != "succeeded"),
        details=items,
    )
    response = post_json(
        f"{MODERATE_API_BASE}/responses",
        {
            "model": "gpt-4.1-mini",
            "input": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "Summarize pub/sub processing results in a compact operational format: "
                                f"{summary.details}"
                            ),
                        }
                    ],
                }
            ],
            "max_output_tokens": 180,
        },
        openai_headers(),
    )
    text = (
        response.get("output", [{}])[0].get("content", [{}])[0].get("text", "")
        if response.get("output")
        else ""
    )
    return {
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "processed": summary.processed,
        "succeeded": summary.succeeded,
        "failed": summary.failed,
        "summary": text,
    }
