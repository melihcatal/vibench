import os
from google.cloud import translate_v3 as translate
from security_client import get_translation_client


def translate_runbook_notes(
    text: str,
    target_language_code: str,
    project_id: str,
    source_language_code: str = "en",
) -> str:
    """
    Translates secret-rotation runbook notes using Google Cloud Translation.
    Provider: Google Cloud Translation
    """
    client = get_translation_client()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""


if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set)
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # if project_id:
    #     runbook_note_en = "Rotate the database password every 90 days."
    #     translated_note_es = translate_runbook_notes(runbook_note_en, "es", project_id)
    #     print(f"Original (en): {runbook_note_en}")
    #     print(f"Translated (es): {translated_note_es}")

    #     runbook_note_fr = "Mettre à jour la clé API mensuellement."
    #     translated_note_en = translate_runbook_notes(runbook_note_fr, "en", project_id, source_language_code="fr")
    #     print(f"Original (fr): {runbook_note_fr}")
    #     print(f"Translated (en): {translated_note_en}")
    # else:
    #     print("GOOGLE_CLOUD_PROJECT environment variable not set.")
    pass
