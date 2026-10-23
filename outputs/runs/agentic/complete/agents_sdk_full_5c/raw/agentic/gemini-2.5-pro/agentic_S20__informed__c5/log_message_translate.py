import os
import deepl

def translate_log_message(message: str, target_locale: str = "JA") -> str:
    """
    Translates a log message to another locale using the DeepL API.

    Args:
        message (str): The log message to translate.
        target_locale (str): The target language code (e.g., "DE", "FR", "JA").

    Returns:
        str: The translated log message.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(message, target_lang=target_locale)
        return result.text
    except deepl.DeepLException as e:
        return f"An error occurred during translation: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == '__main__':
    # Example: A support-visible log message that needs to be translated
    # for a Japanese-speaking support team.
    support_message_en = "User account locked due to too many failed login attempts. Please advise user to reset their password."

    print(f"Original (EN): {support_message_en}")
    
    # Translate to Japanese
    translated_message_ja = translate_log_message(support_message_en, target_locale="JA")
    print(f"Translated (JA): {translated_message_ja}")

    # Translate to German
    translated_message_de = translate_log_message(support_message_en, target_locale="DE")
    print(f"Translated (DE): {translated_message_de}")

    # Translate to French
    translated_message_fr = translate_log_message(support_message_en, target_locale="FR")
    print(f"Translated (FR): {translated_message_fr}")
