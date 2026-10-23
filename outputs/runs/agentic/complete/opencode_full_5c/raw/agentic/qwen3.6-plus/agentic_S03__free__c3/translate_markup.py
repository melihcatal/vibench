from translation_models import MarkupTranslationRequest, TranslationResult
from translation_client import get_openai_client, translate_markup_content


def translate_markup(
    markup: str,
    source_language: str = "auto",
    target_language: str = "en",
    tag_types: list = None,
) -> TranslationResult:
    client = get_openai_client()
    if tag_types is None:
        tag_types = ["html", "xml", "markdown"]
    request = MarkupTranslationRequest(
        markup=markup,
        source_language=source_language,
        target_language=target_language,
        tag_types=tag_types,
    )
    return translate_markup_content(client, request)
