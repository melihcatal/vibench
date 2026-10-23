import os
from google.cloud import translate_v2 as translate
from speech_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    """
    Translates text using Google Cloud Translate API.
    """
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS not set.")

    translate_client = translate.Client()

    result = translate_client.translate(
        request.text, target_language=request.target_language
    )

    return TranslationResponse(translated_text=result["translatedText"])


if __name__ == "__main__":
    # This is an example
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print(
            "Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable for this example."
        )
    else:
        sample_request = TranslationRequest(
            text="Hello, this is a test of the translation service.",
            target_language="es",
        )
        response = translate_text(sample_request)
        print(f"Original: {sample_request.text}")
        print(f"Translated: {response.translated_text}")
