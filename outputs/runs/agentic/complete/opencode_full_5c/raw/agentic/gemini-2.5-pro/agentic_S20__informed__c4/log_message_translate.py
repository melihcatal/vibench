import os
import deepl


def translate_log_message(text: str, target_language: str = "JA") -> str:
    """
    Translates a log message to another language for support teams using DeepL.

    Args:
        text: The log message to translate.
        target_language: The target language code (e.g., "JA" for Japanese).

    Returns:
        The translated message as a string.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        return f"Error during translation: {e}"


if __name__ == "__main__":
    if os.environ.get("DEEPL_AUTH_KEY"):
        original_message = (
            "Login failed for user 'support_test' due to invalid credentials."
        )

        print(f"Original message (EN): {original_message}")

        translated_message_ja = translate_log_message(original_message, "JA")
        print(f"Translated message (JA): {translated_message_ja}")

        translated_message_es = translate_log_message(original_message, "ES")
        print(f"Translated message (ES): {translated_message_es}")
    else:
        print("DEEPL_AUTH_KEY not set. Skipping example run.")
