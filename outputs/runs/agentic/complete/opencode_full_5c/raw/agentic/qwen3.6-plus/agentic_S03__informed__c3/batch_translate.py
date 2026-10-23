import deepl
from translation_client import get_translation_client
from translation_models import (
    BatchTranslationRequest,
    TranslationResponse,
    TranslationResult,
    normalize_language_code,
)


def batch_translate(
    texts: list[str],
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

    results = client.translate_text(texts, target_lang=norm_target, **deepl_kwargs)

    translated_results = []
    for result in results:
        translated_results.append(
            TranslationResult(
                text=result.text,
                detected_source_lang=result.detected_source_lang,
                character_count=len(result.text),
            )
        )

    source_lang_detected = (
        translated_results[0].detected_source_lang if translated_results else ""
    )

    return TranslationResponse(
        results=translated_results,
        source_lang=source_lang_detected,
        target_lang=norm_target,
        total_characters=sum(r.character_count for r in translated_results),
    )
