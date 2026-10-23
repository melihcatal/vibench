import os
import deepl

def translate_alt_text(text: str, target_lang: str = "en") -> str:
    """Translates generated image descriptions (alt-text) using DeepL API."""
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    translator = deepl.Translator(auth_key)

    # DeepL target languages are typically two-letter codes (e.g., "en", "fr", "de")
    # Some also support country-specific variants like "en-US", "en-GB".
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text

if __name__ == '__main__':
    # This example requires DEEPL_AUTH_KEY to be set.
    # description = "Ein flauschige Katze schläft auf einem Bett."
    # translated_description = translate_alt_text(description, target_lang="en-US")
    # print(f"Original: {description}")
    # print(f"Translated: {translated_description}")
    pass
