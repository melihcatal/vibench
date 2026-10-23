import os
import deepl


def translate_log_message(message: str, target_locale: str = "DE") -> str:
    """
    Translates a support-visible log message for another locale using DeepL.

    Args:
        message: The log message to translate.
        target_locale: The target language code (e.g., "DE" for German).

    Returns:
        The translated message.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(message, target_lang=target_locale)
        return result.text
    except deepl.DeepLException as e:
        return f"An error occurred during translation: {e}"


if __name__ == "__main__":
    log_message_en = "User failed to update profile due to insufficient permissions."

    # Translate to German
    translated_message_de = translate_log_message(log_message_en, "DE")
    print(f"Original (EN): {log_message_en}")
    print(f"Translated (DE): {translated_message_de}")

    # Translate to French
    translated_message_fr = translate_log_message(log_message_en, "FR")
    print(f"\nOriginal (EN): {log_message_en}")
    print(f"Translated (FR): {translated_message_fr}")
