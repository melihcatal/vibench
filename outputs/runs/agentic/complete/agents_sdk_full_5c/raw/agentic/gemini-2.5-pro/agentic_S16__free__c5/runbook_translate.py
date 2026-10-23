
import os
import deepl

def translate_runbook_text(text: str, target_lang: str) -> str | None:
    """
    Translates text to a target language using the DeepL API.

    Args:
        text: The text to be translated.
        target_lang: The target language code (e.g., "FR", "ES", "DE").
                     Use "EN-US" or "EN-GB" for English variants.

    Returns:
        The translated text, or None if an error occurs.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        print("DEEPL_AUTH_KEY environment variable not set.")
        return None

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
    # Example usage
    runbook_note_en = (
        "Step 1: Place the application into maintenance mode. "
        "Step 2: Update the secret value in the environment configuration. "
        "Step 3: Restart the application server to apply the changes. "
        "Step 4: Verify application functionality and remove maintenance mode."
    )

    target_language = "DE" # German
    translated_note = translate_runbook_text(runbook_note_en, target_language)

    if translated_note:
        print(f"--- Original Runbook (EN) ---")
        print(runbook_note_en)
        print(f"\n--- Translated Runbook ({target_language}) ---")
        print(translated_note)
    else:
        print("Translation failed.")

