import os

from google.cloud import translate_v2 as translate

from messaging_models import PayloadTranslateRequest, PayloadTranslateResponse


def translate_payload_text(
    request: PayloadTranslateRequest,
) -> PayloadTranslateResponse:
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    # or the service account key file should be available.
    translate_client = translate.Client()

    # Target language can be a ISO 639-1 code (e.g., "es" for Spanish, "fr" for French)
    result = translate_client.translate(
        request.text, target_language=request.target_language
    )

    translated_text = result["translatedText"]

    return PayloadTranslateResponse(translated_text=translated_text)


if __name__ == "__main__":
    # Example Usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set up)
    text_to_translate = "Hello, how are you?"
    target_language = "es"  # Spanish

    request = PayloadTranslateRequest(
        text=text_to_translate, target_language=target_language
    )
    response = translate_payload_text(request)
    print(f"Original text: '{text_to_translate}'")
    print(f"Translated text ({target_language}): '{response.translated_text}'")
