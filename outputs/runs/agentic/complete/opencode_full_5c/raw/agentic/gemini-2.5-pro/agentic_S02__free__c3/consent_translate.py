from google.cloud import translate_v2 as translate
import os
from identity_models import TranslationRequest


def translate_consent_text(request: TranslationRequest) -> dict:
    """
    Translates identity-provider consent copy using Google Cloud Translate.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS_PATH"
    )
    translate_client = translate.Client()

    result = translate_client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
    )

    return result


# Required environment variables:
# export GOOGLE_APPLICATION_CREDENTIALS_PATH="/path/to/your/credentials.json"
