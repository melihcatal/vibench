import os
from messaging_client import AWSMessagingClient
from messaging_models import TranslationRequest, TranslationResult


def translate_payload_text(request: TranslationRequest) -> TranslationResult:
    """Translates customer-facing message payload text using Amazon Translate."""
    translate_client = AWSMessagingClient().get_translate_client()

    try:
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language_code,
            TargetLanguageCode=request.target_language_code,
        )
        translated_text = response["TranslatedText"]
        return TranslationResult(
            translated_text=translated_text,
            source_language_code=request.source_language_code,
            target_language_code=request.target_language_code,
        )
    except Exception as e:
        print(f"Error translating text with Amazon Translate: {e}")
        return TranslationResult(
            translated_text=f"Translation error: {str(e)}",
            source_language_code=request.source_language_code,
            target_language_code=request.target_language_code,
        )


if __name__ == "__main__":
    # Example Usage
    translation_request = TranslationRequest(
        text="Hello, welcome to our store! We have great deals for you.",
        source_language_code="en",
        target_language_code="es",
    )

    translation_result = translate_payload_text(translation_request)
    print("\n--- Translation Result ---")
    print(
        f"Original ({translation_request.source_language_code}): {translation_request.text}"
    )
    print(
        f"Translated ({translation_request.target_language_code}): {translation_result.translated_text}"
    )

    translation_request_de = TranslationRequest(
        text="Ein neuer Artikel wurde in Ihren Warenkorb gelegt.",
        source_language_code="de",
        target_language_code="en",
    )
    translation_result_de = translate_payload_text(translation_request_de)
    print("\n--- Translation Result (German to English) ---")
    print(
        f"Original ({translation_request_de.source_language_code}): {translation_request_de.text}"
    )
    print(
        f"Translated ({translation_request_de.target_language_code}): {translation_result_de.translated_text}"
    )
