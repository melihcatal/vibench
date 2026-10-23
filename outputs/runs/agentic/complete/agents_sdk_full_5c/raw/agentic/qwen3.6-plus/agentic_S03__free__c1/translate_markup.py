"""Translate HTML or markup while preserving tags using AWS Translate."""

import os
import re
import boto3
from botocore.config import Config
from typing import List, Tuple
from translation_client import load_translation_config
from translation_models import TranslationRequest, TranslationResponse, normalize_language_code


HTML_TAG_PATTERN = re.compile(r'(<[^>]+>)')
HTML_ENTITY_PATTERN = re.compile(r'&[a-zA-Z0-9#]+;')


def _extract_text_segments(markup: str) -> Tuple[List[str], List[Tuple[str, int, int]]]:
    """Extract translatable text segments from markup, preserving tag positions.

    Returns:
        Tuple of (text_segments, tag_info) where tag_info contains (tag, start, end).
    """
    segments = []
    tag_info = []
    last_end = 0

    for match in HTML_TAG_PATTERN.finditer(markup):
        text_before = markup[last_end:match.start()]
        if text_before.strip():
            segments.append(text_before)
        tag_info.append((match.group(), match.start(), match.end()))
        last_end = match.end()

    remaining = markup[last_end:]
    if remaining.strip():
        segments.append(remaining)

    return segments, tag_info


def _rebuild_markup(segments: List[str], tag_info: List[Tuple[str, int, int]], original: str) -> str:
    """Rebuild markup with translated segments while preserving tags."""
    result_parts = []
    tag_idx = 0
    seg_idx = 0
    last_pos = 0

    for tag_text, tag_start, tag_end in tag_info:
        text_before = original[last_pos:tag_start]
        if text_before.strip() and seg_idx < len(segments):
            result_parts.append(segments[seg_idx])
            seg_idx += 1
        result_parts.append(tag_text)
        last_pos = tag_end

    if last_pos < len(original) and seg_idx < len(segments):
        result_parts.append(segments[seg_idx])

    return ''.join(result_parts)


def translate_markup(markup_text: str, source_lang: str, target_lang: str) -> TranslationResponse:
    """Translate HTML/markup content preserving tags using AWS Translate.

    Args:
        markup_text: HTML or markup text with tags.
        source_lang: Source language code.
        target_lang: Target language code.

    Returns:
        TranslationResponse with translated markup preserving tags.
    """
    config = load_translation_config()
    aws_region = os.environ.get("AWS_DEFAULT_REGION", config.get("aws_region", "us-east-1"))
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID", config.get("aws_access_key_id"))
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY", config.get("aws_secret_access_key"))

    client_config = Config(
        region_name=aws_region,
        retries={"max_attempts": 3, "mode": "standard"},
    )

    translate_client = boto3.client(
        "translate",
        config=client_config,
        aws_access_key_id=aws_access_key if aws_access_key else None,
        aws_secret_access_key=aws_secret_key if aws_secret_key else None,
    )

    normalized_source = normalize_language_code(source_lang)
    normalized_target = normalize_language_code(target_lang)

    text_segments, tag_info = _extract_text_segments(markup_text)

    if not text_segments:
        return TranslationResponse(
            translated_text=markup_text,
            source_lang=normalized_source,
            target_lang=normalized_target,
            model_used="aws-translate-html",
            confidence=1.0,
            character_count=len(markup_text),
        )

    translated_segments = []
    for segment in text_segments:
        request = TranslationRequest(
            text=segment,
            source_lang=normalized_source,
            target_lang=normalized_target,
            model="aws-general",
        )

        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_lang,
            TargetLanguageCode=request.target_lang,
        )

        translated_segments.append(response["TranslatedText"])

    translated_markup = _rebuild_markup(translated_segments, tag_info, markup_text)

    return TranslationResponse(
        translated_text=translated_markup,
        source_lang=normalized_source,
        target_lang=normalized_target,
        model_used="aws-translate-general",
        confidence=1.0,
        character_count=len(markup_text),
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 4:
        src = sys.argv[1]
        tgt = sys.argv[2]
        text = sys.argv[3]
        result = translate_markup(text, src, tgt)
        print(result.translated_text)
    else:
        print("Usage: translate_markup.py <source_lang> <target_lang> <markup>")
