from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,
    TextCategory,
    TextBlocklistMatch,
)
from safety_client import get_content_safety_client
from safety_models import TextModerationRequest, RedactionResult


def redact_unsafe(request: TextModerationRequest) -> RedactionResult:
    """
    Flags or redacts unsafe spans from text using Azure AI Content Safety.
    Note: Azure AI Content Safety does not directly provide redacted text in a single API call with character offsets for redaction.
    This function simulates redaction based on detected categories and their severities.
    For true redaction with character offsets, a post-processing step based on blocklist matches or detected categories would be needed.
    """
    client = get_content_safety_client()
    categories = [
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
    ]
    request_body = AnalyzeTextOptions(
        text=request.text, categories=categories, blocklist_names=["MyBlocklist"]
    )  # Assuming a blocklist exists

    response = client.analyze_text(request_body)

    redacted_text = request.text
    blocks = []

    # Simple redaction logic: if any category is above a certain severity, suggest full text might be unsafe
    # For actual span-based redaction, one would use blocklist matches if available or more sophisticated NLP.
    is_unsafe_overall = False
    for category_result in response.categories_analysis:
        if (
            category_result.severity and category_result.severity >= 4
        ):  # Example threshold for redaction
            is_unsafe_overall = True
            blocks.append(
                {
                    "category": category_result.category.value,
                    "severity": category_result.severity,
                    "suggested_action": "redact_full_text",  # Placeholder for actual span info
                }
            )

    if response.blocklist_matches:
        for match in response.blocklist_matches:
            # In a real scenario, use match.offset and match.length to redact specific spans.
            # For simplicity here, just mark the text as needing redaction if a blocklist match occurs.
            is_unsafe_overall = True
            blocks.append(
                {
                    "blocklist_name": match.blocklist_name,
                    "block_item_text": match.block_item_text,
                    "suggested_action": "redact_span",
                    "offset": match.offset,
                    "length": match.length,
                }
            )

    if is_unsafe_overall:
        redacted_text = (
            "[REDACTED]"  # Simple full redaction if any unsafe content is detected.
        )
        # More advanced logic would build redacted_text char by char.

    return RedactionResult(
        original_text=request.text, redacted_text=redacted_text, blocks=blocks
    )
