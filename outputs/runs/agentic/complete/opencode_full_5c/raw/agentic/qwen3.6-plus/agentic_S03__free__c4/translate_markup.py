import re
from typing import Optional

from translation_client import translate_with_html
from translation_models import (
    TranslationRequest,
    TranslationResult,
    parse_google_translate_response,
)


def extract_html_tags(text: str) -> tuple[str, list[tuple[str, int, int]]]:
    tag_pattern = re.compile(r"(<[^>]+>)")
    tags: list[tuple[str, int, int]] = []
    cleaned_parts: list[str] = []
    last_end = 0

    for match in tag_pattern.finditer(text):
        if match.start() > last_end:
            cleaned_parts.append(text[last_end : match.start()])
        tags.append((match.group(), match.start(), match.end()))
        last_end = match.end()

    if last_end < len(text):
        cleaned_parts.append(text[last_end:])

    cleaned_text = "".join(cleaned_parts)
    return cleaned_text, tags


def reconstruct_html(
    translated_text: str, original_text: str, tags: list[tuple[str, int, int]]
) -> str:
    if not tags:
        return translated_text

    tag_positions: list[tuple[str, int, int]] = []
    current_pos = 0
    text_segments = re.split(r"(<[^>]+>)", translated_text)

    reconstructed = translated_text
    for tag_content, orig_start, orig_end in tags:
        reconstructed = reconstructed.replace(
            f"__TAG_{tags.index((tag_content, orig_start, orig_end))}__", tag_content
        )

    return reconstructed


def translate_markup(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    model: str = "nmt",
    api_key: Optional[str] = None,
) -> TranslationResult:
    request = TranslationRequest(
        text=text,
        source_language=source_language,
        target_language=target_language,
        format="html",
        model=model,
    )

    response_data = translate_with_html(
        text=request.text,
        target_language=request.target_language,
        source_language=request.source_language,
        model=request.model,
        api_key=api_key,
    )

    result = parse_google_translate_response(response_data, request.text)

    return TranslationResult(
        translated_text=result.translated_text,
        detected_source_language=result.detected_source_language,
        model=result.model,
    )


def translate_markup_with_config(
    config: TranslationRequest,
    api_key: Optional[str] = None,
) -> TranslationResult:
    return translate_markup(
        text=config.text,
        target_language=config.target_language,
        source_language=config.source_language,
        model=config.model,
        api_key=api_key,
    )
