import os
from typing import Tuple
from moderate_text import moderate_text
from safety_models import ContentSafetyResponse

def redact_unsafe(text: str, threshold: int = 2) -> Tuple[str, bool]:
    """Flags or redacts unsafe spans from text using Azure AI Content Safety for detection.

    Returns the potentially redacted text and a boolean indicating if redaction occurred.
    """
    try:
        moderation_result = moderate_text(text)

        is_unsafe = (
            moderation_result.hate_severity >= threshold or
            moderation_result.self_harm_severity >= threshold or
            moderation_result.sexual_severity >= threshold or
            moderation_result.violence_severity >= threshold
        )

        if is_unsafe:
            # In a real-world scenario, you might use a more advanced service for span-level redaction
            # or leverage Azure's blocklist feature if specific terms are known.
            # For this exercise, we'll indicate redaction by replacing the text.
            redacted_text = "[REDACTED UNSAFE CONTENT]"
            return redacted_text, True
        else:
            return text, False

    except Exception as e:
        print(f"Error during unsafe content detection/redaction: {e}")
        return text, False # Return original text and False for redaction status on error

if __name__ == "__main__":
    # Example usage (requires environment variables AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY)
    # os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "YOUR_ENDPOINT"
    # os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_KEY"
    # test_text_safe = "Hello, how are you?"
    # test_text_unsafe = "I want to hurt myself."

    # redacted_safe, was_redacted_safe = redact_unsafe(test_text_safe)
    # print(f"Original: '{test_text_safe}', Redacted: '{redacted_safe}', Was Redacted: {was_redacted_safe}")

    # redacted_unsafe, was_redacted_unsafe = redact_unsafe(test_text_unsafe)
    # print(f"Original: '{test_text_unsafe}', Redacted: '{redacted_unsafe}', Was Redacted: {was_redacted_unsafe}")
    pass
