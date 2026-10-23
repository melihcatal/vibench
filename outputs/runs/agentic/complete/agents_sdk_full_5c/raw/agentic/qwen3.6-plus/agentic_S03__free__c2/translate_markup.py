"""
translate_markup.py - Translates HTML or markup while preserving tags
using Google Cloud Translation API v3.
"""

from typing import Optional, List, Tuple
from google.cloud import translate_v3 as translate
from html.parser import HTMLParser

from translation_client import get_translation_client, get_project_location, validate_client_ready
from translation_models import (
    TranslationResult,
    normalize_language_code,
    validate_translation_response,
)


class TagPreservationParser(HTMLParser):
    """
    HTML parser that identifies text nodes to translate while preserving
    HTML tag structure and attributes.
    """

    def __init__(self):
        super().__init__()
        self.parts: List[Tuple[str, bool]] = []  # (content, is_tag)

    def handle_starttag(self, tag, attrs):
        attr_str = " ".join(f'{k}="{v}"' for k, v in attrs if v is not None)
        if attr_str:
            self.parts.append((f"<{tag} {attr_str}>", True))
        else:
            self.parts.append((f"<{tag}>", True))

    def handle_endtag(self, tag):
        self.parts.append((f"</{tag}>", True))

    def handle_data(self, data):
        if data.strip():
            self.parts.append((data, False))

    def handle_entityref(self, name):
        self.parts.append((f"&{name};", True))

    def handle_charref(self, name):
        self.parts.append((f"&#{name};", True))


def _rebuild_html(parts: List[Tuple[str, bool]], translated_parts: List[str]) -> str:
    """Rebuild HTML string from parts, replacing text nodes with translations."""
    result = []
    text_idx = 0
    for content, is_tag in parts:
        if is_tag:
            result.append(content)
        else:
            if text_idx < len(translated_parts):
                result.append(translated_parts[text_idx])
                text_idx += 1
            else:
                result.append(content)
    return "".join(result)


def translate_markup(
    html_text: str,
    source_language: str = "auto",
    target_language: str = "es",
    model: str = "nmt",
) -> TranslationResult:
    """
    Translate HTML or markup text while preserving tags using Google Cloud
    Translation API v3.

    Google Cloud Translation v3 accepts HTML content via the mime_type parameter
    set to "text/html" and automatically preserves HTML tags during translation.

    Args:
        html_text: HTML or markup text to translate.
        source_language: Source language code (BCP-47).
        target_language: Target language code (BCP-47).
        model: Translation model identifier ("nmt" for Google Neural MT).

    Returns:
        TranslationResult with translated HTML and metadata.
    """
    if not validate_client_ready():
        raise RuntimeError(
            "Google Cloud Translation client not configured. "
            "Set GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS."
        )

    source_lang = normalize_language_code(source_language)
    target_lang = normalize_language_code(target_language)

    client = get_translation_client()
    parent = get_project_location()

    model_path = f"{parent}/models/{model}" if model != "nmt" else None

    request = translate.TranslateTextRequest(
        contents=[html_text],
        target_language_code=target_lang,
        parent=parent,
        model=model_path,
        mime_type="text/html",
    )

    if source_lang != "auto":
        request.source_language_code = source_lang

    response = client.translate_text(request=request)

    translated_html = response.translations[0].translated_text
    validated = validate_translation_response(translated_html)

    detected_source = None
    if response.translations[0].detected_language_code:
        detected_source = response.translations[0].detected_language_code

    return TranslationResult(
        translated_text=validated if validated else html_text,
        source_language=source_lang,
        target_language=target_lang,
        model=model,
        confidence=0.9,
        detected_source_language=detected_source,
    )


if __name__ == "__main__":
    html_input = "<p>Hello, <strong>world</strong>!</p>"
    result = translate_markup(html_input, target_language="de")
    print(f"Original:  {html_input}")
    print(f"Translated: {result.translated_text}")
