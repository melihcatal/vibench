from translation_client import AzureTranslatorClient
from translation_models import MarkupTranslationRequest, TranslationResponse
from azure.ai.translation.text import models


def translate_markup(request: MarkupTranslationRequest) -> TranslationResponse:
    client = AzureTranslatorClient()

    input_text_element = models.InputTextItem(text=request.html_text)
    response = client.client.translate(
        text_elements=[input_text_element],
        to=[request.to_lang],
        from_parameter=request.from_lang,
        text_type="html",
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
