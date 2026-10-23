from security_client import get_translation_client


def translate_runbook_notes(text: str, target_language: str = "es") -> str:
    """
    Translates secret-rotation runbook notes using Google Cloud Translation API.
    """
    client = get_translation_client()

    result = client.translate(text, target_language=target_language)
    return result["translatedText"]


if __name__ == "__main__":
    runbook_notes_en = "In case of rotation failure, revert to the previous secret version and contact the on-call engineer."

    translated_notes_es = translate_runbook_notes(runbook_notes_en, "es")
    print(f"Original (en): {runbook_notes_en}")
    print(f"Translated (es): {translated_notes_es}")

    translated_notes_fr = translate_runbook_notes(runbook_notes_en, "fr")
    print(f"Translated (fr): {translated_notes_fr}")
