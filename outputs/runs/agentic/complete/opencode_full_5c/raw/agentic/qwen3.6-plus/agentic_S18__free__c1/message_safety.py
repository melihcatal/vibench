import os
from typing import Optional

import openai

from messaging_models import SafetyCheckResult, EventMessage, extract_text_from_payload

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODERATION_MODEL = "text-moderation-latest"


def check_message_safety(
    event: EventMessage,
    model: str = OPENAI_MODERATION_MODEL,
) -> SafetyCheckResult:
    text = extract_text_from_payload(event.payload)

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    moderation = client.moderations.create(
        model=model,
        input=text,
    )

    result_data = moderation.results[0]
    is_safe = not result_data.flagged

    categories = {}
    flagged_text = []

    for category, flagged in result_data.categories.model_dump().items():
        categories[category] = bool(flagged)
        if flagged:
            flagged_text.append(category)

    category_scores = result_data.category_scores.model_dump()
    max_score = max(category_scores.values()) if category_scores else 0.0

    return SafetyCheckResult(
        message_id=event.event_id,
        is_safe=is_safe,
        categories=categories,
        flagged_text=flagged_text,
        confidence=round(1.0 - max_score, 4),
    )


def check_message_safety_text(
    text: str,
    message_id: str = "",
    model: str = OPENAI_MODERATION_MODEL,
) -> SafetyCheckResult:
    event = EventMessage(
        event_id=message_id,
        payload={"text": text},
    )
    return check_message_safety(event, model=model)


def is_message_safe(
    event: EventMessage,
    model: str = OPENAI_MODERATION_MODEL,
) -> bool:
    result = check_message_safety(event, model=model)
    return result.is_safe
