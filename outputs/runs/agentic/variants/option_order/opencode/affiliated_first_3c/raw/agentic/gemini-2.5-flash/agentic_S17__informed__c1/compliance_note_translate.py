import os
from google.cloud import translate_v3
from security_client import TranslationClient
from security_models import TranslationRequest, TranslationResponse


def translate_compliance_note(request: TranslationRequest) -> TranslationResponse:
    client = TranslationClient().client
    project_id = os.environ.get(
        "GOOGLE_CLOUD_PROJECT"
    )  # Assumes GOOGLE_CLOUD_PROJECT env var is set
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    try:
        # Google Cloud Translation: service=Cloud Translation; sdk=google-cloud-translate; auth=GOOGLE_APPLICATION_CREDENTIALS
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [request.text],
                "target_language_code": request.target_language,
                "source_language_code": request.source_language
                if request.source_language
                else None,
            }
        )
        translated_text = response.translations[0].translated_text
        return TranslationResponse(translated_text=translated_text)
    except Exception as e:
        raise RuntimeError(f"Translation failed: {e}")
