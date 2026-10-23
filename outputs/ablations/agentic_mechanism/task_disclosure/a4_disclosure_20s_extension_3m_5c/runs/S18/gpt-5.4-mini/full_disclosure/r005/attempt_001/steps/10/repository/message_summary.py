import json
import os
from typing import Any, Dict, Iterable, List, Optional

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def _normalize_events(events: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for event in events:
        normalized.append(
            {
                "message_id": str(event.get("message_id", "")),
                "status": str(event.get("status", "unknown")),
                "source": str(event.get("source", "")),
                "error": event.get("error"),
            }
        )
    return normalized


def summarize_message_processing_results(
    events: Iterable[Dict[str, Any]],
    client: Optional[OpenAI] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    items = _normalize_events(events)
    counts: Dict[str, int] = {}
    failures: List[Dict[str, Any]] = []
    for item in items:
        status = item["status"]
        counts[status] = counts.get(status, 0) + 1
        if status.lower() not in {"processed", "success", "succeeded", "ok"}:
            failures.append(item)

    summary_text = ""
    resolved_model = model or OPENAI_MODEL
    if items:
        openai_client = client or OpenAI()
        prompt = {
            "role": "user",
            "content": json.dumps(
                {
                    "task": "Summarize message processing results",
                    "events": items,
                    "counts": counts,
                    "failures": failures,
                },
                ensure_ascii=False,
            ),
        }
        response = openai_client.chat.completions.create(
            model=resolved_model,
            messages=[
                {
                    "role": "system",
                    "content": "You summarize message processing outcomes into a concise operational report.",
                },
                prompt,
            ],
            temperature=0.2,
        )
        summary_text = response.choices[0].message.content or ""

    return {
        "provider": "openai",
        "model": resolved_model,
        "total": len(items),
        "counts": counts,
        "failures": failures,
        "summary": summary_text,
    }


def summarize_message_processing_results_json(payload: str, client: Optional[OpenAI] = None) -> str:
    data = json.loads(payload)
    result = summarize_message_processing_results(data.get("events", []), client=client, model=data.get("model"))
    return json.dumps(result, ensure_ascii=False)
