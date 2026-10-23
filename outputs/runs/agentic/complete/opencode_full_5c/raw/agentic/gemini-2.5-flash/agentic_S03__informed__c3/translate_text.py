from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = TranslationClient()
    translate_client = client.get_client()
    parent = client.get_parent()

    response = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language,
            "source_language_code": request.source_language,
            "mime_type": request.mime_type,
        }
    )

    translated_text = response.translations[0].translated_text
    detected_source_language = response.translations[0].detected_language_code

    return TranslationResponse(translated_text, detected_source_language)
