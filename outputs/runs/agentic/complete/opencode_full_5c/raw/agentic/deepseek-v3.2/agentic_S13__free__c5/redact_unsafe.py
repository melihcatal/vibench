import os
from typing import List, Dict, Any, Tuple
from openai import OpenAI
import re


def redact_unsafe(text: str) -> Dict[str, Any]:
    """
    Flags or redacts unsafe spans from text using OpenAI's moderation API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    moderation_response = client.moderations.create(
        model="text-moderation-latest", input=text
    )

    result = moderation_response.results[0]

    if not result.flagged:
        return {
            "original_text": text,
            "redacted_text": text,
            "flagged": False,
            "redacted_spans": [],
        }

    flagged_categories = []
    for category_name, is_flagged in result.categories.model_dump().items():
        if is_flagged:
            flagged_categories.append(category_name)

    redacted_text = text
    redacted_spans = []

    if flagged_categories:
        completion_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a content moderation assistant. Identify and redact unsafe spans in the given text. Return the redacted text with [REDACTED] markers.",
                },
                {
                    "role": "user",
                    "content": f"Text: {text}\nFlagged categories: {', '.join(flagged_categories)}\nPlease redact unsafe spans.",
                },
            ],
            temperature=0.1,
        )

        redacted_text = completion_response.choices[0].message.content

        pattern = r"\[REDACTED\]"
        matches = list(re.finditer(pattern, redacted_text))
        for match in matches:
            redacted_spans.append(
                {
                    "start": match.start(),
                    "end": match.end(),
                    "replacement": match.group(),
                }
            )

    return {
        "original_text": text,
        "redacted_text": redacted_text,
        "flagged": result.flagged,
        "flagged_categories": flagged_categories,
        "redacted_spans": redacted_spans,
        "category_scores": result.category_scores.model_dump(),
    }
