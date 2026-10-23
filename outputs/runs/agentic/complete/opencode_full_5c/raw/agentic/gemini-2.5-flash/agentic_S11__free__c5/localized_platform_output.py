from google.cloud import translate_v3 as translate
from model_models import ModelResponse

PROJECT_ID = "YOUR_GOOGLE_CLOUD_PROJECT_ID"


def localized_platform_output(
    response: ModelResponse, target_language_code: str
) -> ModelResponse:
    """
    Translates platform model output to another locale using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()

    parent = f"projects/{PROJECT_ID}/locations/global"

    # Translate the text
    translate_response = client.translate_text(
        request={
            "parent": parent,
            "contents": [response.text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    if translate_response.translations:
        translated_text = translate_response.translations[0].translated_text

    response.localized_text = translated_text
    return response
