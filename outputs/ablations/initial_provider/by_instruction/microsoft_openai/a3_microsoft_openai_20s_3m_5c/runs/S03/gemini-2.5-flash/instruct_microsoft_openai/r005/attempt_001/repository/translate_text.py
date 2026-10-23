import os
from openai import OpenAI

def translate_text(text: str, source_language: str, target_language: str) -> str:
    """
    Translates a single text string between languages using OpenAI.

    Args:
        text: The text string to translate.
        source_language: The language of the input text (e.g., "en", "fr").
        target_language: The language to translate the text into (e.g., "es", "de").

    Returns:
        The translated text string.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a highly accurate translation service. Translate the following text from {source_language} to {target_language}. Only return the translated text."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()
