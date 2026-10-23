import os
import deepl


def translate_log_message(text: str, target_locale: str) -> str:
    """
    Translates a log message to a target locale using the DeepL API.

    :param text: The log message to translate.
    :param target_locale: The target language code (e.g., "FR", "DE", "JA").
    :return: The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_locale)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred during translation: {e}")
        return f"Translation failed: {e}"


if __name__ == "__main__":
    log_to_translate = "Alert: User login failed due to invalid credentials."
    target_language = "ES"  # Spanish

    print(f"Original (EN): {log_to_translate}")

    try:
        translated_log = translate_log_message(log_to_translate, target_language)
        print(f"Translated ({target_language}): {translated_log}")
    except ValueError as e:
        print(e)

    # Example with a different language
    target_language_jp = "JA"  # Japanese
    try:
        translated_log_jp = translate_log_message(log_to_translate, target_language_jp)
        print(f"Translated ({target_language_jp}): {translated_log_jp}")
    except ValueError as e:
        print(e)
