from translation_client import get_translate_client
from translation_models import TranslationRequest, TranslationResponse
from google.cloud.translate_v3.types import TranslateTextRequest


def batch_translate(
    texts: list[str], target_language: str, source_language: str = None
) -> list[str]:
    client = get_translate_client()
    parent = f"projects/{client.project_id}"
    request = TranslateTextRequest(
        parent=parent,
        contents=texts,
        target_language_code=target_language,
        source_language_code=source_language if source_language else None,
        mime_type="text/plain",
    )
    response = client.translate_text(request=request)
    return TranslationResponse(
        [translation.translated_text for translation in response.translations]
    ).to_list()
