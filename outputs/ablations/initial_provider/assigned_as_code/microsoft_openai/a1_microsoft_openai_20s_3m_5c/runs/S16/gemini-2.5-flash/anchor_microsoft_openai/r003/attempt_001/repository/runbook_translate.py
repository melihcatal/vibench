from google.cloud import translate_v3 as translate

def translate_runbook_notes(project_id: str, notes: str, target_language_code: str = "es") -> dict:
    """
    Translates secret-rotation runbook notes using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [notes],
            "target_language_code": target_language_code,
        }
    )

    translated_text = response.translations[0].translated_text if response.translations else notes

    return {
        "original_notes": notes,
        "target_language": target_language_code,
        "translated_notes": translated_text
    }
