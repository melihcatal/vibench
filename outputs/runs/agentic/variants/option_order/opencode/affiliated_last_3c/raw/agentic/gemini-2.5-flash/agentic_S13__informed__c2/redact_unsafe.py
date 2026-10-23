import os
from typing import Dict, Any, List
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from safety_client import get_content_safety_client
from safety_models import RedactRequest, RedactResponse, ModerationCategory


def redact_unsafe(request: RedactRequest) -> RedactResponse:
    client = get_content_safety_client()

    categories = [
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
        TextCategory.SELF_HARM,
    ]

    request_body = AnalyzeTextOptions(text=request.text, categories=categories)
    response = client.analyze_text(request_body)

    redacted_text = request.text
    detected_spans: List[Dict[str, Any]] = []
    is_unsafe = False

    if response.categories_analysis:
        for category_analysis in response.categories_analysis:
            mod_category = None
            if category_analysis.category == TextCategory.HATE:
                mod_category = ModerationCategory.HATE
            elif category_analysis.category == TextCategory.SEXUAL:
                mod_category = ModerationCategory.SEXUAL
            elif category_analysis.category == TextCategory.VIOLENCE:
                mod_category = ModerationCategory.VIOLENCE
            elif category_analysis.category == TextCategory.SELF_HARM:
                mod_category = ModerationCategory.SELF_HARM

            if (
                mod_category
                and mod_category in request.categories_to_redact
                and category_analysis.severity > 0
            ):
                is_unsafe = True
                # For simplicity, if any category to redact is found, we redact the entire text.
                # Azure Content Safety does not provide span-level redaction for text analysis.
                # In a real-world scenario, a different service or custom logic would be needed for span-level redaction.
                detected_spans.append(
                    {
                        "category": mod_category.value,
                        "severity": category_analysis.severity,
                        "text": request.text,
                        "offset": 0,
                        "length": len(request.text),
                    }
                )
                # Only redact once, if any applicable category is found
                if is_unsafe:
                    break

    if is_unsafe:
        redacted_text = "[REDACTED]"

    return RedactResponse(
        original_text=request.text,
        redacted_text=redacted_text,
        detected_spans=detected_spans,
    )
