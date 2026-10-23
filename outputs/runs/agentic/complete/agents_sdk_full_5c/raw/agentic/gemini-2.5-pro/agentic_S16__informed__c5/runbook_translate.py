"""Translate secret-rotation runbook notes using DeepL."""
import os
import deepl
from typing import Optional

def translate_runbook(text: str, target_lang: str) -> Optional[str]:
    """
    Translates a runbook text to a target language using the DeepL API.

    Args:
        text: The text to be translated.
        target_lang: The target language code (e.g., "DE", "FR", "ES").

    Returns:
        The translated text as a string, or None if an error occurs.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred with the DeepL API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == '__main__':
    runbook_notes_en = """
    Step 1: Manually trigger the secret rotation Lambda function.
    Step 2: Verify that the application successfully connects using the new credentials.
    Step 3: If the connection fails, immediately revert to the previous secret version using the 'AWSPREVIOUS' label.
    """

    target_language = "DE"  # German

    translated_notes = translate_runbook(runbook_notes_en, target_language)

    if translated_notes:
        print(f"--- Original English Text ---")
        print(runbook_notes_en)
        print(f"\n--- Translated German Text ---")
        print(translated_notes)
    else:
        print("Translation failed. Please check your DEEPL_AUTH_KEY and API plan.")
