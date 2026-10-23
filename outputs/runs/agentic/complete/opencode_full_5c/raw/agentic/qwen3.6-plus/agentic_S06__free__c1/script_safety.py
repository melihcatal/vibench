from __future__ import annotations

from speech_client import create_openai_client, OPENAI_MODERATION_MODEL
from speech_models import SafetyCheckRequest, SafetyCheckResponse, normalize_text


def check_script_safety(
    text: str,
    model: str | None = None,
    api_key: str | None = None,
) -> SafetyCheckResponse:
    normalized = normalize_text(text)
    if not normalized:
        raise ValueError("Input text is empty")

    selected_model = model or OPENAI_MODERATION_MODEL

    client = create_openai_client(api_key=api_key)

    moderation = client.moderations.create(
        input=normalized,
        model=selected_model,
    )

    result = moderation.results[0]

    categories = {}
    flagged_categories = []

    for category_name, is_flagged in result.categories.model_dump().items():
        categories[category_name] = bool(is_flagged)
        if is_flagged:
            flagged_categories.append(category_name)

    is_safe = not result.flagged

    return SafetyCheckResponse(
        is_safe=is_safe,
        categories=categories,
        flagged_categories=flagged_categories,
        model=selected_model,
    )
