import os
import deepl
from typing import Optional


def translate_runbook_entry(text: str, target_lang: str = "DE") -> Optional[str]:
    """
    Translates secret-rotation runbook notes using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred with DeepL API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    runbook_note_en = "Emergency rollback procedure: Manually revert the secret to the previous version (AWSPREVIOUS stage) and restart the application services."
    target_language = "ES"  # Spanish

    print(f"Original (EN): {runbook_note_en}")
    translated_note = translate_runbook_entry(
        runbook_note_en, target_lang=target_language
    )

    if translated_note:
        print(f"Translated ({target_language}): {translated_note}")
    else:
        print(f"Translation to {target_language} failed.")
