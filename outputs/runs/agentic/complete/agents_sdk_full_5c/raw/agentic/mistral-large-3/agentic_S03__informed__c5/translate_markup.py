from translation_client import GoogleTranslationClient
from translation_models import MarkupTranslationRequest, MarkupTranslationResponse


def translate_markup(markup: str, target_lang: str, source_lang: str = None, protected_tags: list = None) -> MarkupTranslationResponse:
    client = GoogleTranslationClient()
    request = MarkupTranslationRequest(
        markup=markup,
        source_lang=source_lang,
        target_lang=target_lang,
        protected_tags=protected_tags or [],
    )
    return client.translate_markup(request)