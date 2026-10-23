import deepl
from translation_client import get_translation_client
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    TranslationResult,
    normalize_language_code,
)


def translate_text(
    text: str,
    source_lang: str | None = None,
    target_lang: str = "en",
    formality: str | None = None,
    preserve_formatting: bool = True,
) -> TranslationResponse:
    client: deepl.Translator = get_translation_client()

    norm_source = normalize_language_code(source_lang) if source_lang else None
    norm_target = normalize_language_code(target_lang)

    deepl_kwargs = {}
    if norm_source:
        deepl_kwargs["source_lang"] = norm_source
    if formality:
        deepl_kwargs["formality"] = formality
    deepl_kwargs["preserve_formatting"] = preserve_formatting

    result = client.translate_text(text, target_lang=norm_target, **deepl_kwargs)

    translation_result = TranslationResult(
        text=result.text,
        detected_source_lang=result.detected_source_lang,
        character_count=len(result.text),
    )

    return TranslationResponse(
        results=[translation_result],
        source_lang=result.detected_source_lang,
        target_lang=norm_target,
        total_characters=translation_result.character_count,
    )
