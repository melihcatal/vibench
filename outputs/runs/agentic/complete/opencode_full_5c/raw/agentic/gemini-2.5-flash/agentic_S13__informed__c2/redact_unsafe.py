from safety_client import get_content_safety_client
from safety_models import RedactionResult
from azure.ai.contentsafety.models import AnalyzeTextOptions


def redact_unsafe(text: str, redaction_character: str = "*") -> RedactionResult:
    client = get_content_safety_client()
    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    categories_detected = []
    should_redact = False
    for result in response.categories_analysis:
        if result.severity > 0:
            should_redact = True
            categories_detected.append(result.category.value)

    redacted_text = text
    if should_redact:
        redacted_text = redaction_character * len(text)

    return RedactionResult(
        original_text=text,
        redacted_text=redacted_text,
        categories_detected=categories_detected,
    )
