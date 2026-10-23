import os
from ibm_watsonx_ai.hlp.text import TextPrompt, TextChatClient
from ibm_watsonx_ai.hlp.content_safety import ContentSafetyClient


def check_unsafe_copy(translated_texts: list[str]) -> list[bool]:
    """
    Checks localized copy for unsafe content using watsonx content safety.

    Args:
        translated_texts: List of translated strings.

    Returns:
        List of booleans indicating whether each text is safe (True) or unsafe (False).
    """
    safety_client = ContentSafetyClient()
    results = []
    for text in translated_texts:
        # Uses watsonx guardrails endpoint internally
        response = safety_client.analyze_content(text)
        # Assume response has a boolean `safe` field
        results.append(response.safe)
    return results
