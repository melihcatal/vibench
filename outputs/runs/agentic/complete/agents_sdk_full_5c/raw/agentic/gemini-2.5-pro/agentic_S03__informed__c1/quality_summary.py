"""
Summarize translation quality issues using an Anthropic model.
"""
import os
from anthropic import Anthropic

def summarize_translation_quality(source_text: str, translated_text: str) -> str:
    """
    Uses Anthropic's Claude 3 Sonnet to summarize potential quality issues in a translation.

    Args:
        source_text: The original text.
        translated_text: The translated text.

    Returns:
        A summary of potential quality issues.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = Anthropic(api_key=api_key)

    prompt = f"""
Please review the following translation for quality. Identify any potential issues such as mistranslations, grammatical errors, awkward phrasing, or loss of nuance. Provide a brief summary of your findings.

Source Text:
"{source_text}"

Translated Text:
"{translated_text}"

Summary of Quality Issues:
"""

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=500,
        temperature=0.2,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    return message.content[0].text
