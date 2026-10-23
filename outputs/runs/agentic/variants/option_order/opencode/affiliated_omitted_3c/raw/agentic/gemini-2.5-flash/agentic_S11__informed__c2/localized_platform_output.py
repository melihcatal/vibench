from model_client import get_translate_client
from model_models import TranslationRequest, TranslationResponse
import os


def translate_platform_output(request: TranslationRequest) -> TranslationResponse:
    """
    Translate platform model output for another locale using Amazon Translate.
    """
    client = get_translate_client()

    response = client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_lang,
        TargetLanguageCode=request.target_lang,
    )
    return TranslationResponse(response)


if __name__ == "__main__":
    # Example usage:
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION are set in environment variables
    translation_request = TranslationRequest(
        text="Hello, how are you?", source_lang="en", target_lang="es"
    )
    translation_response = translate_platform_output(translation_request)
    print(f"Original text: {translation_request.text}")
    print(f"Translated text (Spanish): {translation_response.translated_text}")

    translation_request_fr = TranslationRequest(
        text="What is your name?", source_lang="en", target_lang="fr"
    )
    translation_response_fr = translate_platform_output(translation_request_fr)
    print(f"Original text: {translation_request_fr.text}")
    print(f"Translated text (French): {translation_response_fr.translated_text}")
