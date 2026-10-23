import os
from google.cloud import translate_v3 as translate
from messaging_models import TranslationRequest


def translate_payload_text(request: TranslationRequest) -> dict:
    """Translates customer-facing message payload text using Google Cloud Translation.

    Args:
        request: A TranslationRequest object containing the text and target language.

    Returns:
        A dictionary with the translated text and detected source language.
    """
    client = translate.TranslationServiceClient()
    project_id = os.getenv("GCP_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError(
            "GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT environment variable not set."
        )

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [request.text],
                "target_language_code": request.target_language_code,
                "source_language_code": request.source_language_code,  # Optional
                "mime_type": "text/plain",
            }
        )

        translated_text = response.translations[0].translated_text
        detected_source_language = response.translations[0].detected_language_code

        return {
            "translated_text": translated_text,
            "detected_source_language": detected_source_language,
        }
    except Exception as e:
        print(f"Error translating text with Google Cloud Translation: {e}")
        return {"error": f"Could not translate text. {e}"}
