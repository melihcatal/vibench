from safety_client import ContentSafetyClientWrapper
from safety_models import TextContent, ModerationResult, RedactionResult


def redact_unsafe_text(user_text: str) -> RedactionResult:
    client_wrapper = ContentSafetyClientWrapper()
    text_content = TextContent(text=user_text)
    moderation_result = client_wrapper.moderate_text(text_content)

    redacted_text = user_text
    unsafe_spans = []

    if moderation_result.is_unsafe:
        # For demonstration, if any category is unsafe, we 'redact' the entire text.
        # A real-world scenario would require more sophisticated span-level detection.
        redacted_text = "*" * len(user_text)
        for category_detection in moderation_result.categories_detection:
            if category_detection.severity > 0:
                # In a real scenario, this would be precise offsets from the service.
                # Here, we're just indicating that the category makes the text unsafe.
                unsafe_spans.append(
                    {
                        "category": category_detection.category,
                        "severity": category_detection.severity,
                    }
                )

    return RedactionResult(
        original_text=user_text, redacted_text=redacted_text, unsafe_spans=unsafe_spans
    )
