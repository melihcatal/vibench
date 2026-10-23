import os
from translation_client import create_translator_client
import translation_models as tm

def translate_text(source_text: str, target_lang: str = "es") -> str:
    """Translate a single text string using Azure AI Translator.
    Args:
        source_text: The source text to translate.
        target_lang: Target language code (e.g., 'es' for Spanish).
    Returns:
        The translated text.
    """
    client = create_translator_client()
    response = client.translate(
        texts=[source_text],
        to_language=target_lang
    )
    translated = response[0].translations[0].text
    return translated

if __name__ == "__main__":
    sample = "Hello, world!"
    print(f"Original: {sample}")
    print(f"Translated: {translate_text(sample)}")
