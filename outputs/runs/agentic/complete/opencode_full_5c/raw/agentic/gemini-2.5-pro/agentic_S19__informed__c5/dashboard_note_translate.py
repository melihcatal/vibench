import os
import deepl


def translate_note(text: str, target_language: str = "FR") -> str:
    """
    Translates a dashboard note or metric description to another language using DeepL.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., "FR" for French, "ES" for Spanish).

    Returns:
        The translated text as a string.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        return f"An error occurred during translation: {e}"


if __name__ == "__main__":
    note = "High CPU utilization detected on production servers."

    # Translate to French
    translated_note_fr = translate_note(note, "FR")
    print(f'Original (EN): "{note}"')
    print(f'Translated (FR): "{translated_note_fr}"')

    # Translate to Spanish
    translated_note_es = translate_note(note, "ES")
    print(f'Translated (ES): "{translated_note_es}"')
