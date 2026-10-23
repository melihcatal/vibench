import os
import deepl

def translate_appeal_text(text: str, target_lang: str = "EN-US") -> str:
    """
    Translate appeal text for review by a global team.

    Args:
        text: The text of the user's appeal.
        target_lang: The target language code (e.g., "EN-US", "DE", "FR").

    Returns:
        The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        # Fallback to returning original text on error
        return text
