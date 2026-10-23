from google.cloud import translate_v3
import os


def translate_compliance_note(
    text: str, target_language: str, project_id: str = None, source_language: str = None
) -> dict:
    """Translates encryption or compliance notes using Google Cloud Translation."""
    if project_id is None:
        project_id = os.getenv("GCP_TRANSLATION_PROJECT_ID")
        if project_id is None:
            project_id = os.getenv(
                "GCP_PROJECT_ID"
            )  # Fallback to general GCP project ID

    if not project_id:
        raise ValueError(
            "Google Cloud Project ID for translation must be provided or set as environment variable GCP_TRANSLATION_PROJECT_ID or GCP_PROJECT_ID."
        )

    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
            "source_language_code": source_language if source_language else "",
        }
    )

    translated_text = response.translations[0].translated_text
    detected_source_language = (
        response.translations[0].detected_language_code
        if not source_language
        else source_language
    )

    return {
        "translated_text": translated_text,
        "detected_source_language": detected_source_language,
    }
