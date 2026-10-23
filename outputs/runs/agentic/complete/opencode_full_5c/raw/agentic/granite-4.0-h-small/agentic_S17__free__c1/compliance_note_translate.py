# [LATER-STEP] compliance_note_translate.py
# Translates encryption or compliance notes between languages using OpenAI ChatGPT API
import os
import openai
from typing import TypedDict


class TranslationInput(TypedDict):
    content: str
    target_language: str  # e.g., "es", "fr", "de"


def load_openai_config() -> None:
    """Ensures the OpenAI API key is set in the environment.

    Raises RuntimeError if not present.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "Set OPENAI_API_KEY environment variable to use translation service"
        )


def translate_note(input: TranslationInput) -> str:
    """Translates a compliance note using OpenAI's translation endpoint.

    Args:
        input: dict with keys 'content' (original note) and 'target_language' (ISO code).
    Returns:
        Translated note as a string.
    """
    load_openai_config()
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a precise translator. Ensure technical terminology related to encryption and compliance is accurately conveyed.",
            },
            {
                "role": "user",
                "content": f"Translate the following text to {input['target_language']}:\n\n{input['content']}",
            },
        ],
        temperature=0.2,
    )
    translated = response.choices[0].message.content.strip()
    return translated


if __name__ == "__main__":
    # Example usage
    note_en = "The data is encrypted with AES-256-GCM using a KMS-managed key."
    translated = translate_note({"content": note_en, "target_language": "es"})
    print("Translated note:", translated)
