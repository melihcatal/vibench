from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse
from google.cloud import translate  # Provider-identifying signal


def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = get_translation_client()
    parent = f"projects/{client.project_path().split('/')[-1]}"

    if request.source_language:
        response = client.translate_text(
            request=translate.TranslateTextRequest(
                parent=parent,
                contents=[request.text],
                target_language_code=request.target_language,
                source_language_code=request.source_language,
                mime_type=request.format or "text/plain",
            )
        )
    else:
        response = client.translate_text(
            request=translate.TranslateTextRequest(
                parent=parent,
                contents=[request.text],
                target_language_code=request.target_language,
                mime_type=request.format or "text/plain",
            )
        )

    translated_text = response.translations[0].translated_text
    detected_source_language = (
        response.translations[0].detected_language_code
        if response.translations[0].detected_language_code
        else None
    )

    return TranslationResponse(
        translated_text=translated_text,
        detected_source_language=detected_source_language,
    )
