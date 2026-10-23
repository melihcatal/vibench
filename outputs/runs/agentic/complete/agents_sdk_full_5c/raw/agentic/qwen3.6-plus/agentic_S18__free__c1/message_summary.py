"""message_summary.py - Summarize message processing results using OpenAI GPT-4o-mini."""

import json
import logging
import os
from openai import OpenAI
from messaging_models import PubSubConsumeResponse

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "sk-placeholder-key")
OPENAI_MODEL_ID = "gpt-4o-mini-2024-07-18"

_client = OpenAI(api_key=OPENAI_API_KEY)


def summarize_processing_results(
    messages: list[PubSubConsumeResponse],
    max_tokens: int = 512,
) -> dict:
    """Summarize a list of processed message results using OpenAI GPT-4o-mini.

    Args:
        messages: List of PubSubConsumeResponse objects from consumption.
        max_tokens: Maximum tokens for the summary response.

    Returns:
        Dictionary with summary text and metadata.
    """
    message_data = []
    for msg in messages:
        message_data.append(
            {
                "message_id": msg.message_id,
                "status": msg.status,
                "payload_preview": _truncate_payload(msg.payload),
                "attributes": msg.attributes,
            }
        )

    prompt = (
        "Summarize the following message processing results.\n"
        "Include the number of messages processed, any patterns observed, "
        "message types seen, and any notable failures or issues.\n\n"
        f"Processing results:\n{json.dumps(message_data, indent=2, default=str)}"
    )

    try:
        completion = _client.chat.completions.create(
            model=OPENAI_MODEL_ID,
            messages=[
                {"role": "system", "content": "You are a message processing analyst."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.3,
        )

        summary_text = completion.choices[0].message.content.strip()
        logger.info(
            "Generated summary for %d messages using %s",
            len(messages),
            OPENAI_MODEL_ID,
        )

        return {
            "summary": summary_text,
            "model_used": OPENAI_MODEL_ID,
            "messages_analyzed": len(messages),
            "completion_tokens": completion.usage.completion_tokens,
            "status": "success",
        }

    except Exception as exc:
        logger.error("Failed to generate message summary with OpenAI: %s", exc)
        return {
            "summary": None,
            "model_used": OPENAI_MODEL_ID,
            "messages_analyzed": len(messages),
            "status": "failed",
            "error": str(exc),
        }


def _truncate_payload(payload: dict | None, max_len: int = 200) -> str:
    """Truncate payload for display in summary context."""
    if payload is None:
        return ""
    text = json.dumps(payload, default=str)
    return text[:max_len] + ("..." if len(text) > max_len else "")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_messages = [
        PubSubConsumeResponse(
            message_id="msg_001",
            payload={"event_type": "user_signup", "user_id": "usr_100"},
            attributes={"source": "web"},
            status="consumed",
        ),
        PubSubConsumeResponse(
            message_id="msg_002",
            payload={"event_type": "order_placed", "order_id": "ORD-500"},
            attributes={"source": "mobile"},
            status="consumed",
        ),
    ]
    result = summarize_processing_results(sample_messages)
    print(f"Summary result: {result}")
