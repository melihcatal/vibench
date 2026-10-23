
import os
import deepl

def translate_log_message(message: str, target_language_code: str = "DE") -> str:
    """
    Translates a log message to a specified target language using the DeepL API.

    Args:
        message: The log message text to translate.
        target_language_code: The target language code (e.g., "DE" for German, "FR" for French).

    Returns:
        The translated message string, or an error message if translation fails.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(message, target_lang=target_language_code)
        return result.text
    except deepl.DeepLException as e:
        return f"DeepL API error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == '__main__':
    # This message might be displayed to a German-speaking support agent.
    original_message = "User 'jdoe' failed to authenticate due to an invalid password."
    
    print(f"Original message (EN): {original_message}")
    
    translated_message = translate_log_message(original_message, "DE")
    
    print(f"Translated message (DE): {translated_message}")

    translated_message_fr = translate_log_message(original_message, "FR")
    print(f"Translated message (FR): {translated_message_fr}")
