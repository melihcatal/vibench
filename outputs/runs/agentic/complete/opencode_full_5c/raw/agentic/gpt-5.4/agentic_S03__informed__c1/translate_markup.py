from __future__ import annotations

from translation_client import get_deepl_client
from translation_models import TranslationRequest, translation_item_from_deepl


def translate_markup(
    markup: str,
    source_language: str,
    target_language: str,
    markup_kind: str = "html",
):
    request = TranslationRequest(
        text=markup,
        source_language=source_language,
        target_language=target_language,
        tag_handling=markup_kind,
    )
    translator = get_deepl_client()
    result = translator.translate_text(request.text, **request.to_deepl_kwargs())
    return translation_item_from_deepl(result, billed_characters=len(markup))
