from google.cloud import translate_v3 as translate
import os
from model_models import PlatformTranslationRequest, PlatformTranslationResponse


def translate_platform_output(
    request: PlatformTranslationRequest,
) -> PlatformTranslationResponse:
    client = translate.TranslationServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language_code,
            "source_language_code": request.source_language_code
            if request.source_language_code
            else None,
        }
    )

    translated_text = response.translations[0].translated_text
    detected_language_code = (
        response.translations[0].detected_language_code
        if response.translations[0].detected_language_code
        else None
    )

    return PlatformTranslationResponse(
        translated_text=translated_text,
        detected_language_code=detected_language_code,
        provider="Google Cloud Translation API",
    )
