from typing import List
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from safety_client import get_content_safety_client
from safety_models import RedactionResponse, RedactionResult


def redact_unsafe_text(text: str, redaction_threshold: int = 4) -> RedactionResponse:
    client = get_content_safety_client()
    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    redaction_details = []
    is_unsafe = False
    for category_result in response.categories_analysis:
        if category_result.severity >= redaction_threshold:
            is_unsafe = True
        redaction_details.append(
            RedactionResult(
                category=category_result.category.value,
                severity=category_result.severity,
                detected=category_result.severity > 0,
            )
        )

    redacted_text = "[REDACTED]" if is_unsafe else text

    return RedactionResponse(
        text=text, redacted_text=redacted_text, redaction_details=redaction_details
    )
