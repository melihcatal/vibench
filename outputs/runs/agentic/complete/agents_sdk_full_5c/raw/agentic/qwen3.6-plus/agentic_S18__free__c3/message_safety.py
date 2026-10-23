"""Check message payload text for unsafe content using OpenAI moderation.

Uses OpenAI Moderation API as the concrete external provider.
"""

import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

from messaging_models import EventMessage, MessageResponse


OPENAI_MODEL_ID = os.environ.get("OPENAI_MODERATION_MODEL", "text-moderation-latest")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def _get_openai_client() -> OpenAI:
    """Create and return an OpenAI client for moderation checks."""
    return OpenAI(api_key=OPENAI_API_KEY)


def _extract_text_from_payload(payload: Dict[str, Any]) -> str:
    """Extract meaningful text content from a message payload dict."""
    text_parts: List[str] = []
    for key in ("text", "message", "content", "body", "description", "comment"):
        val = payload.get(key)
        if val and isinstance(val, str):
            text_parts.append(val)
    if not text_parts:
        text_parts.append(str(payload))
    return " ".join(text_parts)


def check_message_safety(
    event: EventMessage,
    model: Optional[str] = None,
) -> MessageResponse:
    """Check a message payload for unsafe content using OpenAI moderation.

    Args:
        event: The EventMessage to check.
        model: The OpenAI moderation model ID to use.

    Returns:
        MessageResponse with safety assessment details.
    """
    model_id = model or OPENAI_MODEL_ID

    try:
        client = _get_openai_client()
        text_to_check = _extract_text_from_payload(event.payload)

        if not text_to_check.strip():
            return MessageResponse(
                success=True,
                event_id=event.event_id,
                details={
                    "safe": True,
                    "reason": "Empty or non-text payload, no moderation needed",
                    "model": model_id,
                    "provider": "openai",
                },
            )

        moderation = client.moderations.create(
            input=text_to_check,
            model=model_id,
        )

        result = moderation.results[0]
        flagged = result.flagged
        categories = result.categories.model_dump() if hasattr(result.categories, "model_dump") else {}
        category_scores = result.category_scores.model_dump() if hasattr(result.category_scores, "model_dump") else {}

        flagged_categories = [cat for cat, is_flagged in categories.items() if is_flagged]

        return MessageResponse(
            success=True,
            event_id=event.event_id,
            details={
                "safe": not flagged,
                "flagged": flagged,
                "flagged_categories": flagged_categories,
                "categories": categories,
                "category_scores": category_scores,
                "model": model_id,
                "provider": "openai",
            },
        )
    except Exception as exc:
        return MessageResponse(
            success=False,
            event_id=event.event_id,
            error=str(exc),
            details={"provider": "openai", "model": model_id},
        )


def check_text_safety(
    text: str,
    model: Optional[str] = None,
) -> MessageResponse:
    """Check raw text for unsafe content using OpenAI moderation.

    Args:
        text: The text content to check.
        model: The OpenAI moderation model ID to use.

    Returns:
        MessageResponse with safety assessment.
    """
    model_id = model or OPENAI_MODEL_ID

    try:
        client = _get_openai_client()

        moderation = client.moderations.create(
            input=text,
            model=model_id,
        )

        result = moderation.results[0]

        return MessageResponse(
            success=True,
            details={
                "safe": not result.flagged,
                "flagged": result.flagged,
                "model": model_id,
                "provider": "openai",
            },
        )
    except Exception as exc:
        return MessageResponse(
            success=False,
            error=str(exc),
            details={"provider": "openai", "model": model_id},
        )
