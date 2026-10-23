import os
from translation_client import TranslationClient

def translate_text(source_text: str, target_lang: str = "es") -> str:
    """Translate a single text string to the target language.

    Args:
        source_text: The source string to translate.
        target_lang: Target language code (ISO 639-1).
    Returns:
        Translated text.
    """
    client = TranslationClient()
    # Ensure the target language is supported by the provider's preset list.
    if target_lang not in client.supported_languages:
        raise ValueError(f"Target language {target_lang} not supported.")
    response = client.translate(source_text, target_lang)
    # The client returns a dict with the translated string under "translatedText".
    return response.get("translatedText", source_text)

# Example usage (can be removed in production)
if __name__ == "__main__":
    test = "Hello, world!"
    print(translate_text(test, "fr"))
