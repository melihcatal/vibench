"""message_safety.py - Check message payload text for unsafe content using OpenAI Moderation API."""

import json
import logging
import os
from openai import OpenAI
from messaging_models import PubSubConsumeResponse

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "sk-placeholder-key")
OPENAI_MODERATION_MODEL = "omni-moderation-latest"

_client = OpenAI(api_key=OPENAI_API_KEY)


def check_message_safety(message_response: PubSubConsumeResponse) -> dict:
    """Check the message payload for unsafe content using OpenAI Moderation API.

    Args:
        message_response: A PubSubConsumeResponse containing the message payload.

    Returns:
        Dictionary with safety flags, categories, and verdict.
    """
    if message_response.payload is None:
        return {
            "message_id": message_response.message_id,
            "is_safe": True,
            "flags": [],
            "categories": {},
            "status": "no_content",
        }

    text_to_check = _extract_text_from_payload(message_response.payload)

    if not text_to_check:
        return {
            "message_id": message_response.message_id,
            "is_safe": True,
            "flags": [],
            "categories": {},
            "status": "no_text_content",
        }

    try:
        moderation_result = _client.moderations.create(
            input=text_to_check,
            model=OPENAI_MODERATION_MODEL,
        )

        result = moderation_result.results[0]
        is_flagged = result.flagged

        flagged_categories = []
        categories = {}

        for category, is_flagged_cat in result.categories.model_dump().items():
            if is_flagged_cat:
                flagged_categories.append(category)
            categories[category] = is_flagged_cat

        logger.info(
            "Safety check for message_id=%s: flagged=%s, categories=%s",
            message_response.message_id,
            is_flagged,
            flagged_categories,
        )

        return {
            "message_id": message_response.message_id,
            "is_safe": not is_flagged,
            "flags": flagged_categories,
            "categories": categories,
            "status": "checked",
            "model_used": OPENAI_MODERATION_MODEL,
        }

    except Exception as exc:
        logger.error("Safety check failed with OpenAI moderation: %s", exc)
        return {
            "message_id": message_response.message_id,
            "is_safe": True,
            "flags": [],
            "categories": {},
            "status": "failed",
            "error": str(exc),
        }


def _extract_text_from_payload(payload: dict) -> str:
    """Extract relevant text content from a message payload dictionary."""
    text_parts = []

    for key in ["text", "message", "body", "content", "description", "comment"]:
        if key in payload:
            val = payload[key]
            if isinstance(val, str):
                text_parts.append(val)

    if not text_parts:
        text_parts.append(json.dumps(payload, default=str))

    return " ".join(text_parts)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_msg = PubSubConsumeResponse(
        message_id="msg_safety_001",
        payload={"text": "This is a normal friendly message for testing.", "user": "alice"},
        attributes={"source": "chat"},
        status="consumed",
    )
    result = check_message_safety(sample_msg)
    print(f"Safety check result: {result}")
