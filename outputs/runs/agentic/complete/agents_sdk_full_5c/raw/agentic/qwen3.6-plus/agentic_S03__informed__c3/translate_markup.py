"""Translate HTML or markup while preserving tags.

Provider: DeepL API (deepl SDK)
Auth: DEEPL_AUTH_KEY
"""

from typing import Optional

from translation_client import get_client
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    build_request,
    deepl_result_to_response,
)


def translate_markup(
    text: str,
    source_lang: str = "",
    target_lang: str = "EN",
    formality: str = "default",
) -> TranslationResponse:
    """Translate HTML/markup content using DeepL with tag_handling='html'.

    DeepL's tag_handling parameter preserves HTML/XML tags during translation.

    Args:
        text: HTML or markup text to translate.
        source_lang: Source language code. Auto-detected if empty.
        target_lang: Target language code. Defaults to 'EN'.
        formality: Formality level for the translation.

    Returns:
        TranslationResponse with translated markup preserving tags.
    """
    req = build_request(
        text=text,
        source_lang=source_lang,
        target_lang=target_lang,
        formality=formality,
    )

    client = get_client()
    result = client.translate(
        text=req.text,
        source_lang=req.source_lang,
        target_lang=req.target_lang,
        formality=req.formality,
        tag_handling="html",
    )

    return deepl_result_to_response(result, target_lang=req.target_lang)


def translate_xml_markup(
    text: str,
    source_lang: str = "",
    target_lang: str = "EN",
    formality: str = "default",
    ignore_tags: Optional[list[str]] = None,
    non_splitting_tags: Optional[list[str]] = None,
) -> TranslationResponse:
    """Translate XML-style markup with fine-grained tag control via DeepL.

    Args:
        text: XML or markup text to translate.
        source_lang: Source language code. Auto-detected if empty.
        target_lang: Target language code. Defaults to 'EN'.
        formality: Formality level for the translation.
        ignore_tags: Tags whose content should not be translated.
        non_splitting_tags: Tags that should not cause sentence splitting.

    Returns:
        TranslationResponse with translated markup preserving XML tags.
    """
    import deepl

    auth_key = __import__("os").environ.get("DEEPL_AUTH_KEY", "")
    client = deepl.Translator(auth_key)

    kwargs: dict = {
        "target_lang": target_lang.upper(),
        "tag_handling": "xml",
    }
    if source_lang:
        kwargs["source_lang"] = source_lang.upper()
    if formality != "default":
        kwargs["formality"] = formality
    if ignore_tags:
        kwargs["ignore_tags"] = ignore_tags
    if non_splitting_tags:
        kwargs["non_splitting_tags"] = non_splitting_tags

    result = client.translate_text(text, **kwargs)

    return deepl_result_to_response(result, target_lang=target_lang)
