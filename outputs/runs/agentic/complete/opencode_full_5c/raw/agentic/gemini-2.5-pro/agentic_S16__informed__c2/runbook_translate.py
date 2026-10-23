import os
import deepl


def translate_runbook_entry(text: str, target_language: str = "JA") -> str | None:
    """
    Translates a runbook entry to the specified target language using DeepL.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred during translation: {e}")
        return None


if __name__ == "__main__":
    runbook_note_en = "Emergency rollback procedure: Revert the 'AWSCURRENT' staging label to the previous secret version ID."

    translated_note = translate_runbook_entry(runbook_note_en)

    if translated_note:
        print(f"Original (EN): {runbook_note_en}")
        print(f"Translated (JA): {translated_note}")
    else:
        print("Translation failed.")
