
import os
import deepl


def translate_dashboard_note(text: str, target_lang: str) -> str:
    """
    Translates a dashboard note or metric annotation to another language
    using the DeepL API.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "DE", "FR", "ES").

    Returns:
        The translated text as a string.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        return f"An error occurred during translation: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


if __name__ == '__main__':
    note_en = (
        "Alert threshold breached for CPU utilization on production servers. "
        "Investigating potential memory leak."
    )
    
    target_language = "DE" # German
    
    print(f"Original (EN): {note_en}")
    
    translated_note = translate_dashboard_note(note_en, target_language)
    
    print(f"Translated ({target_language}): {translated_note}")

    target_language_fr = "FR" # French
    translated_note_fr = translate_dashboard_note(note_en, target_language_fr)
    print(f"Translated ({target_language_fr}): {translated_note_fr}")
