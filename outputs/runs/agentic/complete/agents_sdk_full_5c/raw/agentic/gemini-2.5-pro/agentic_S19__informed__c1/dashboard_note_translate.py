import os
import deepl

def translate_dashboard_note(note: str, target_locale: str) -> str:
    """
    Translate metric or dashboard notes for another locale using DeepL.

    Args:
        note: The text content of the note to translate.
        target_locale: The target language code (e.g., "DE", "FR", "JA").

    Returns:
        The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        
        # Ensure target locale is supported by the DeepL library enum
        # This maps a string like "EN-US" to the deepl.Language.ENGLISH_AMERICAN enum
        try:
            target_language_enum = deepl.language.Language(target_locale.upper())
        except ValueError:
            # Fallback for simple codes like "EN", "DE"
            simple_code = target_locale.split('-')[0].upper()
            target_language_enum = deepl.language.Language(simple_code)

        result = translator.translate_text(note, target_lang=target_language_enum)
        
        if isinstance(result, deepl.TextResult):
            return result.text
        # Handle list of results if input was a list (not the case here)
        elif isinstance(result, list) and result:
             return result[0].text
        else:
            return "Translation failed to return a result."

    except deepl.DeepLException as e:
        return f"An error occurred with the DeepL API: {e}"
    except ValueError as e:
        return f"Invalid target locale '{target_locale}': {e}"


if __name__ == '__main__':
    # This is an example and will not be executed in the test environment.
    english_note = "Alert: CPU utilization has exceeded 90% for the last 15 minutes on production servers."
    target_lang = "DE" # German

    print(f"Original note (EN): {english_note}")
    try:
        translated_note = translate_dashboard_note(english_note, target_lang)
        print(f"Translated note ({target_lang}): {translated_note}")
    except ValueError as e:
        print(f"Configuration Error: {e}")

    # Example with unsupported language code to show error handling
    print("\n--- Testing invalid locale ---")
    invalid_lang = "XX"
    error_message = translate_dashboard_note(english_note, invalid_lang)
    print(f"Translation result for invalid locale '{invalid_lang}': {error_message}")
