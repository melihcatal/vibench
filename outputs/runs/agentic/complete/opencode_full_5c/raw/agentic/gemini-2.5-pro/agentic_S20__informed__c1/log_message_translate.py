import os
import deepl


def translate_log_message(message: str, target_locale: str) -> str:
    """
    Translates a log message to another locale using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)

        # Check account usage
        usage = translator.get_usage()
        if usage.any_limit_reached:
            print("Translation limit reached.")
            return f"Error: Translation limit reached."

        result = translator.translate_text(message, target_lang=target_locale)
        return result.text

    except deepl.DeepLException as e:
        print(f"An error occurred with the DeepL API: {e}")
        return f"Error: Could not translate message. {e}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"Error: An unexpected error occurred during translation."


if __name__ == "__main__":
    # Example usage:
    # Set DEEPL_AUTH_KEY in your environment
    log_message_en = "CRITICAL: User data backup failed due to insufficient disk space."

    # Translate to German
    target_lang_de = "DE"
    translated_message_de = translate_log_message(log_message_en, target_lang_de)
    print(f"Original (EN): {log_message_en}")
    print(f"Translated (DE): {translated_message_de}")

    # Translate to Japanese
    target_lang_ja = "JA"
    translated_message_ja = translate_log_message(log_message_en, target_lang_ja)
    print(f"Original (EN): {log_message_en}")
    print(f"Translated (JA): {translated_message_ja}")
