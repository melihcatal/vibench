from translation_client import get_client
from translation_models import TranslationRequest


def translate_text(
    text: str,
    source_lang: str = "auto",
    target_lang: str = "en",
    formality: str | None = None,
) -> str:
    client = get_client()
    request = TranslationRequest(
        text=text,
        source_lang=source_lang,
        target_lang=target_lang,
        formality=formality,
    )
    response = client.translate(request)
    return response.translated_text
