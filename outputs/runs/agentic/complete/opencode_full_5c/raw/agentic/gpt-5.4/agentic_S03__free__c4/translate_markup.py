from __future__ import annotations

from translation_client import deepl_translate
from translation_models import normalize_language_code, normalize_translation_result


def translate_markup(
    markup: str, source_language: str | None, target_language: str
) -> dict[str, str | None]:
    normalized_source = normalize_language_code(source_language)
    normalized_target = normalize_language_code(target_language) or target_language
    item = deepl_translate(
        [markup],
        normalized_target,
        normalized_source,
        tag_handling="html",
    )[0]
    return normalize_translation_result(
        text=item["text"],
        provider="deepl",
        source_language=normalized_source,
        target_language=normalized_target,
        detected_language=item.get("detected_source_language"),
    )
