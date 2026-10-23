from translation_client import get_translate_client
from translation_models import TranslationRequest, TranslationResponse
from google.cloud.translate_v3.types import TranslateTextRequest


def translate_markup(
    markup_text: str, target_language: str, source_language: str = None
) -> str:
    client = get_translate_client()
    parent = f"projects/{client.project_id}"
    request = TranslateTextRequest(
        parent=parent,
        contents=[markup_text],
        target_language_code=target_language,
        source_language_code=source_language if source_language else None,
        mime_type="text/html",  # Specify HTML for markup
    )
    response = client.translate_text(request=request)
    return TranslationResponse(
        [translation.translated_text for translation in response.translations]
    ).to_list()[0]
