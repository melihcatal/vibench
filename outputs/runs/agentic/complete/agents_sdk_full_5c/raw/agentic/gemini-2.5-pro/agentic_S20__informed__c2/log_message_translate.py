import os
import deepl

def translate_log_message(text: str, target_lang: str = "JA") -> str:
    """
    Translates a log message to another language using the DeepL API.

    Args:
        text: The log message text to translate.
        target_lang: The target language code (e.g., "JA" for Japanese).

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
    except deepl.DeepLException as e:
        print(f"An error occurred during translation: {e}")
        return f"Translation failed: {e}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred."


if __name__ == '__main__':
    # Example log message visible to a support team
    support_message = "User 'jdoe' reported an 'Invalid Session ID' error when accessing the dashboard."
    
    print(f"Original message (EN): {support_message}")
    
    # Translate to Japanese for a regional support team
    translated_message = translate_log_message(support_message, "JA")
    
    print(f"Translated message (JA): {translated_message}")
