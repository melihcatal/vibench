from translation_client import AzureTranslatorClient
from translation_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = AzureTranslatorClient()
    response = client.client.translate(
        text_elements=[request.text],
        to=[request.to_lang],
        from_parameter=request.from_lang,
    )

    if response and response[0].translations:
        translated_text = response[0].translations[0].text
        detected_language = (
            response[0].detected_language.language
            if response[0].detected_language
            else None
        )
        return TranslationResponse(
            translated_text=translated_text, detected_language=detected_language
        )
    else:
        return TranslationResponse(translated_text="", detected_language=None)
