import os
from google.cloud import translate_v3 as translate
from messaging_models import TranslationResult

def translate_payload_text(text: str, target_language_code: str, project_id: str = None) -> TranslationResult:
    if not project_id:
        project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable or argument not set.")

    client = translate.TranslationServiceClient()
    location = "global" # Global endpoint for general translation
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    if not response.translations:
        raise RuntimeError("Translation failed or returned no results.")

    translation = response.translations[0]

    return TranslationResult(
        translated_text=translation.translated_text,
        source_language=translation.detected_language_code,
        target_language=target_language_code
    )
