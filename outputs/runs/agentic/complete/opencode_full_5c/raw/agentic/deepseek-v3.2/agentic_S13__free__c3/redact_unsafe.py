import os
import re
from openai import OpenAI
from typing import List, Tuple, Dict, Any


def redact_unsafe(text: str) -> Dict[str, Any]:
    """
    Flag or redact unsafe spans from text using OpenAI's moderation API.
    Returns redacted text and flagged spans.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    moderation_response = client.moderations.create(
        model="text-moderation-latest", input=text
    )

    result = moderation_response.results[0]

    if not result.flagged:
        return {
            "redacted_text": text,
            "flagged_spans": [],
            "flagged_categories": [],
            "was_flagged": False,
        }

    flagged_categories = []
    for category_name, is_flagged in [
        ("hate", result.categories.hate),
        ("hate/threatening", result.categories.hate_threatening),
        ("harassment", result.categories.harassment),
        ("harassment/threatening", result.categories.harassment_threatening),
        ("self-harm", result.categories.self_harm),
        ("self-harm/intent", result.categories.self_harm_intent),
        ("self-harm/instructions", result.categories.self_harm_instructions),
        ("sexual", result.categories.sexual),
        ("sexual/minors", result.categories.sexual_minors),
        ("violence", result.categories.violence),
        ("violence/graphic", result.categories.violence_graphic),
    ]:
        if is_flagged:
            flagged_categories.append(category_name)

    redacted_text = text
    flagged_spans = []

    if flagged_categories:
        redacted_text = "[REDACTED: " + ", ".join(flagged_categories) + "]"
        flagged_spans.append(
            {
                "start": 0,
                "end": len(text),
                "categories": flagged_categories,
                "original_text": text,
            }
        )

    return {
        "redacted_text": redacted_text,
        "flagged_spans": flagged_spans,
        "flagged_categories": flagged_categories,
        "was_flagged": result.flagged,
    }
