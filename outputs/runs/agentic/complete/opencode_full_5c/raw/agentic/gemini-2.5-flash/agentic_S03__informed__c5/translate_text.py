from translation_client import get_translate_client
from translation_models import TranslationRequest, TranslationResponse
from google.cloud import translate_v3beta1 as translate


def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = get_translate_client()
    parent = f"projects/{client.project}"

    response = client.translate_text(
        request=translate.TranslateTextRequest(
            parent=parent,
            contents=[request.text],
            target_language_code=request.target_language,
            source_language_code=request.source_language
            if request.source_language
            else None,
            mime_type="text/plain",  # Use text/html for HTML content
        )
    )

    translated_text = response.translations[0].translated_text
    detected_source_language = response.translations[0].detected_language_code

    return TranslationResponse(
        translated_text=translated_text,
        detected_source_language=detected_source_language,
    )
