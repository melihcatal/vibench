"""
Translates support-visible log messages using the DeepL API.
"""
import os
import deepl

def translate_log_message(text: str, target_lang: str = "DE") -> str:
    """
    Translates a given text to the target language using DeepL.

    Requires the DEEPL_AUTH_KEY environment variable.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        return "Error: DEEPL_AUTH_KEY environment variable not set."

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        return f"Error during translation: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


if __name__ == "__main__":
    original_message = "Permission denied: The user does not have access to this resource."
    target_language = "ES" # Spanish

    print(f"Original (EN): {original_message}")
    translated_message = translate_log_message(original_message, target_lang=target_language)
    print(f"Translated ({target_language}): {translated_message}")

    target_language_german = "DE"
    translated_message_german = translate_log_message(original_message, target_lang=target_language_german)
    print(f"Translated ({target_language_german}): {translated_message_german}")
