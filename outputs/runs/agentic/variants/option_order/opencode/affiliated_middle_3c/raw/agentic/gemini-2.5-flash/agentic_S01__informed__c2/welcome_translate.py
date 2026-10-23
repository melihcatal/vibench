from google.cloud import translate_v2 as translate
from identity_models import TranslationRequest, TranslationResponse
import os


def welcome_translate(request: TranslationRequest) -> TranslationResponse:
    # Google Cloud Translation: service=Cloud Translation; sdk=google-cloud-translate; interface=sdk; auth=GOOGLE_APPLICATION_CREDENTIALS
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    translate_client = translate.Client()

    result = translate_client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
    )

    return TranslationResponse(translated_text=result["translatedText"])
