import os
from google.cloud import translate_v3
from safety_client import get_translate_client # To ensure provider signal linkage
from safety_models import TranslationRequest, TranslationResult

def translate_appeal_text(request: TranslationRequest) -> TranslationResult:
    """
    Translates appeal text for review using Google Cloud Translation API.
    """
    client = get_translate_client()
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language_code,
            "source_language_code": request.source_language_code,
        }
    )

    translated_text = response.translations[0].translated_text
    detected_language = response.translations[0].detected_language_code if response.translations else None

    return TranslationResult(translated_text=translated_text, detected_language_code=detected_language)

if __name__ == '__main__':
    # Example usage:
    # Ensure GCP_PROJECT_ID is set and gcloud authentication is configured.
    # appeal_request = TranslationRequest(
    #     text="Este es un texto de apelación en español.",
    #     target_language_code="en"
    # )
    # translated_response = translate_appeal_text(appeal_request)
    # print(f"Translated text: {translated_response.translated_text}")
    # print(f"Detected language: {translated_response.detected_language_code}")
    pass
