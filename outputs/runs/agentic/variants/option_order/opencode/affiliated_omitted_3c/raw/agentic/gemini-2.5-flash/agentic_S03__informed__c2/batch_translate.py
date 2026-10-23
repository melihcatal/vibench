from translation_client import AzureTranslatorClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    client = AzureTranslatorClient()
    text_elements = request.texts
    to_langs = [request.to_lang]

    response = client.client.translate(
        text_elements=text_elements, to=to_langs, from_parameter=request.from_lang
    )

    translated_texts = []
    detected_languages = []

    if response:
        for translation_item in response:
            if translation_item.translations:
                translated_texts.append(translation_item.translations[0].text)
                detected_languages.append(
                    translation_item.detected_language.language
                    if translation_item.detected_language
                    else None
                )
            else:
                translated_texts.append("")
                detected_languages.append(None)

    return BatchTranslationResponse(
        translations=translated_texts, detected_languages=detected_languages
    )
