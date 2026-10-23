import os
import deepl

def translate_payload_text(text: str, target_lang: str = "en") -> str:
    """Translates customer-facing message payload text using the DeepL API.

    Args:
        text: The text content from the message payload to translate.
        target_lang: The target language code (e.g., 'en', 'fr', 'es'). Defaults to 'en'.

    Returns:
        The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except Exception as e:
        return f"Error translating text: {e}"

if __name__ == '__main__':
    # Example usage
    french_text = "Bonjour le monde! Comment allez-vous?"
    german_text = "Hallo Welt! Wie geht es Ihnen?"

    print(f"Translated (French to English): {translate_payload_text(french_text, target_lang='en')}")
    print(f"Translated (German to Spanish): {translate_payload_text(german_text, target_lang='es')}")
