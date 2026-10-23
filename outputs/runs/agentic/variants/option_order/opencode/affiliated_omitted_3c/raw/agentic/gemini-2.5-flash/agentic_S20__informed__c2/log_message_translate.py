import os
import deepl


def translate_message(log_message_text: str, target_lang: str = "es") -> str:
    """
    Translates support-visible log messages for another locale using DeepL API.
    Requires DEEPL_AUTH_KEY environment variable.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(log_message_text, target_lang=target_lang)
        return result.text
    except Exception as e:
        return f"Error translating message with DeepL: {e}"


if __name__ == "__main__":
    # Example Usage:
    sample_message = "User login failed due to invalid credentials."
    target_language = "fr"  # French

    print(f"\n--- Translating message to {target_language.upper()} ---")
    translated_text = translate_message(sample_message, target_lang=target_language)
    print(f"Original: {sample_message}")
    print(f"Translated ({target_language.upper()}): {translated_text}")

    sample_message_es = "La conexión a la base de datos ha fallado."
    target_language_en = "en-US"  # English (American)
    print(f"\n--- Translating message to {target_language_en.upper()} ---")
    translated_text_en = translate_message(
        sample_message_es, target_lang=target_language_en
    )
    print(f"Original: {sample_message_es}")
    print(f"Translated ({target_language_en.upper()}): {translated_text_en}")
