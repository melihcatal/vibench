from translation_client import GoogleTranslateClient
from translation_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    client_wrapper = GoogleTranslateClient()
    client = client_wrapper.get_client()
    parent = client_wrapper.get_parent()

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language,
            "source_language_code": request.source_language
            if request.source_language
            else None,
            "mime_type": "text/plain",
        }
    )

    translated_text = response.translations[0].translated_text
    detected_language = response.translations[0].detected_language_code

    return TranslationResponse(
        translated_text=translated_text, detected_source_language=detected_language
    )
