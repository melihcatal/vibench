"""Summarize message processing results.

Uses OpenAI API (openai library) as the concrete external provider for AI-powered summarization.
"""

import os
import json
from typing import Any, Dict, List, Optional

from openai import OpenAI

from messaging_models import EventMessage, MessageResponse


OPENAI_MODEL_ID = os.environ.get("OPENAI_MODEL_ID", "gpt-4o-mini")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def _get_openai_client() -> OpenAI:
    """Create and return an OpenAI client."""
    return OpenAI(api_key=OPENAI_API_KEY)


def summarize_processing_results(
    processing_results: List[Dict[str, Any]],
    model: Optional[str] = None,
) -> MessageResponse:
    """Use OpenAI to summarize a list of message processing results.

    Args:
        processing_results: List of dicts with message processing outcome info.
        model: The OpenAI model ID to use for summarization.

    Returns:
        MessageResponse containing the summary text.
    """
    model_id = model or OPENAI_MODEL_ID

    try:
        client = _get_openai_client()

        results_json = json.dumps(processing_results, default=str, indent=2)

        prompt = (
            f"Summarize the following message processing results. "
            f"Provide a concise overview including total count, success rate, "
            f"common event types, and any notable errors or patterns.\n\n"
            f"Results:\n{results_json}"
        )

        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a messaging system analyst. "
                        "Summarize message processing results clearly and concisely."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=500,
        )

        summary_text = response.choices[0].message.content

        return MessageResponse(
            success=True,
            details={
                "summary": summary_text,
                "model": model_id,
                "provider": "openai",
                "total_results": len(processing_results),
            },
        )
    except Exception as exc:
        return MessageResponse(
            success=False,
            error=str(exc),
            details={"provider": "openai", "model": model_id},
        )


def summarize_event_batch(
    events: List[EventMessage],
    processing_status: List[str],
    model: Optional[str] = None,
) -> MessageResponse:
    """Summarize a batch of events with their processing statuses using OpenAI.

    Args:
        events: List of EventMessage objects processed.
        processing_status: List of status strings corresponding to each event.
        model: The OpenAI model ID to use.

    Returns:
        MessageResponse containing the summary.
    """
    results = []
    for event, status in zip(events, processing_status):
        results.append({
            "event_id": event.event_id,
            "event_type": event.event_type,
            "status": status,
            "source": event.source,
            "payload_keys": list(event.payload.keys()) if event.payload else [],
        })

    return summarize_processing_results(results, model=model)
