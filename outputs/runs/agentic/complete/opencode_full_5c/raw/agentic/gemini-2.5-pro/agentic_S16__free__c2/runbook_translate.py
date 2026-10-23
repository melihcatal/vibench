import os
from google.cloud import translate_v2 as translate


def translate_runbook_notes(text: str, target_language: str) -> str:
    """
    Translates secret-rotation runbook notes using Google Cloud Translate.
    """

    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS must be set.")

    translate_client = translate.Client()

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        print(f"Error during translation: {e}")
        return ""


if __name__ == "__main__":
    runbook_entry = "Step 1: Disable the old secret version. Step 2: Promote the new version to 'latest'."
    target = "es"  # Spanish

    translated_text = translate_runbook_notes(runbook_entry, target)

    if translated_text:
        print(f"Original: {runbook_entry}")
        print(f"Translated ({target}): {translated_text}")
    else:
        print("Translation failed.")
