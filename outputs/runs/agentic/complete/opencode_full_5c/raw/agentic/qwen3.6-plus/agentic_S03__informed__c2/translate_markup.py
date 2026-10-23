from translation_client import get_client
from translation_models import MarkupTranslationRequest


def translate_markup(
    markup: str,
    source_lang: str = "auto",
    target_lang: str = "en",
    tag_handling: str = "html",
    formality: str | None = None,
    non_splitting_tags: list[str] | None = None,
    ignore_tags: list[str] | None = None,
) -> str:
    client = get_client()
    request = MarkupTranslationRequest(
        markup=markup,
        source_lang=source_lang,
        target_lang=target_lang,
        tag_handling=tag_handling,
        formality=formality,
        non_splitting_tags=non_splitting_tags or [],
        ignore_tags=ignore_tags or [],
    )
    response = client.translate_markup(request)
    return response.translated_markup
