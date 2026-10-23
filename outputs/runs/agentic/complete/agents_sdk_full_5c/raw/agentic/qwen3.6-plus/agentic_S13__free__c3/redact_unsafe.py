"""Flag or redact unsafe spans from text using OpenAI Moderation API."""

import os
from typing import List, Tuple

from openai import OpenAI

from safety_client import get_safety_config
from safety_models import RedactionRequest, RedactionResponse, normalize_openai_categories


CATEGORY_REDACTION_TOKENS = {
    "hate": "[HATE_REDACTED]",
    "hate/threatening": "[HATE_THREAT_REDACTED]",
    "self-harm": "[SELF_HARM_REDACTED]",
    "self-harm/intent": "[SELF_HARM_INTENT_REDACTED]",
    "self-harm/instructions": "[SELF_HARM_INSTRUCTIONS_REDACTED]",
    "sexual": "[SEXUAL_REDACTED]",
    "sexual/minors": "[SEXUAL_MINORS_REDACTED]",
    "violence": "[VIOLENCE_REDACTED]",
    "violence/graphic": "[VIOLENCE_GRAPHIC_REDACTED]",
}


def redact_unsafe(
    text: str,
    redact_token: str = "[REDACTED]",
    categories_to_redact: List[str] | None = None,
) -> RedactionResponse:
    """Flag or redact unsafe spans from text.

    Uses OpenAI's text-moderation-latest model hosted at api.openai.com to detect
    unsafe categories and redact flagged content segments.

    Args:
        text: The input text to check and redact.
        redact_token: Token to replace unsafe spans. Defaults to [REDACTED].
        categories_to_redact: Specific categories to redact. If None, all flagged categories are redacted.

    Returns:
        RedactionResponse with original text, redacted text, flagged categories, and confidence scores.
    """
    config = get_safety_config()
    client = OpenAI(api_key=config.get("openai_api_key", os.environ.get("OPENAI_API_KEY", "")))

    request = RedactionRequest(
        model="text-moderation-latest",
        input=text,
        redact_token=redact_token,
    )

    moderation_response = client.moderations.create(
        model=request.model,
        input=request.input,
    )

    result = moderation_response.results[0]
    categories = normalize_openai_categories(result.categories)
    category_scores = normalize_openai_categories(result.category_scores, as_float=True)

    flagged_cats = [cat for cat, is_flagged in categories.items() if is_flagged]
    if categories_to_redact:
        flagged_cats = [cat for cat in flagged_cats if cat in categories_to_redact]

    if flagged_cats and result.flagged:
        token = CATEGORY_REDACTION_TOKENS.get(
            flagged_cats[0], redact_token
        )
        redacted_text = token
    else:
        redacted_text = text

    return RedactionResponse(
        original_text=text,
        redacted_text=redacted_text,
        flagged_categories=flagged_cats,
        category_scores=category_scores,
        was_modified=redacted_text != text,
        model="text-moderation-latest",
        provider="openai",
        provider_endpoint="api.openai.com",
    )


if __name__ == "__main__":
    import sys
    sample = sys.argv[1] if len(sys.argv) > 1 else "Check this content for safety."
    result = redact_unsafe(sample)
    print(result.to_dict())
