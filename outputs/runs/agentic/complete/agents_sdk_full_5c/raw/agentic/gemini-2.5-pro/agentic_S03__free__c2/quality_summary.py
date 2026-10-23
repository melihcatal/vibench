import anthropic
from translation_client import ANTHROPIC_API_KEY

def summarize_translation_quality(source_text: str, translated_text: str, source_lang: str, target_lang: str) -> str:
    """
    Uses Anthropic's Claude model to provide a quality summary of a translation.

    Args:
        source_text: The original text.
        translated_text: The translated text.
        source_lang: The source language name (e.g., "English").
        target_lang: The target language name (e.g., "Spanish").

    Returns:
        A summary of the translation's quality.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""
Please evaluate the quality of the following translation from {source_lang} to {target_lang}.

**Source Text ({source_lang}):**
"{source_text}"

**Translated Text ({target_lang}):**
"{translated_text}"

Provide a brief summary of the translation quality, focusing on accuracy, fluency, and any potential awkward phrasing or errors.
"""

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        temperature=0.2,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    
    if message.content and len(message.content) > 0:
        return message.content[0].text.strip()
    return "Could not get a quality summary."
