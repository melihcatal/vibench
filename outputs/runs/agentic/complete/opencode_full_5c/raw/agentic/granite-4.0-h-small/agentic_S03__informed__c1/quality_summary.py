import os
from ibm_watsonx_ai.hlp.text import TextPrompt, TextChatClient


def summarize_quality_issues(
    translated_texts: list[str], original_texts: list[str]
) -> str:
    """
    Summarizes translation quality issues using watsonx guardrails / HAP detection.

    Args:
        translated_texts: List of translated strings.
        original_texts: List of source strings (same order).

    Returns:
        A concise markdown summary of detected quality issues.
    """
    # Initialize the chat client (uses WATSONX_API_KEY & WATSONX_PROJECT_ID env vars)
    client = TextChatClient()
    system_msg = TextPrompt(
        content="You are a translation quality analyst. Evaluate the provided translations and originals for quality issues such as mistranslation, grammatical errors, omissions, and unnatural phrasing. Return a markdown bullet list of each issue with the original and translated snippet."
    )
    summary = []
    for orig, trans in zip(original_texts, translated_texts):
        user_msg = TextPrompt(
            content=f"Translate quality analysis:\nOriginal: {orig}\nTranslated: {trans}"
        )
        response = client.chat(system=system_msg, user=user_msg)
        summary.append(
            f"- **Issue:** {response.text.strip()}\n  **Original:** {orig}\n  **Translated:** {trans}\n"
        )
    return "\\n".join(summary)
