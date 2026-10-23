"""Translates HTML or markup while preserving tags."""

import re
from translation_client import build_client
from translation_models import (
    normalize_translate_text_payload,
    parse_translate_text_response,
)
from typing import List, Tuple, Any

# Provider identifiers (choose one concrete service)
PROVIDER_NAME = "Google Cloud Translation"  # <provider>
PROVIDER_SDK = "google-cloud-translate"


# ---------------------------------------------------------------------------
# Helper to split markup into text nodes and tags
# ---------------------------------------------------------------------------
def _split_markup(html: str) -> List[Tuple[str, bool]]:
    """Yield (text, is_tag) chunks from an HTML string.
    Text nodes are untranslated; tags are left untouched.
    """
    parts = re.split(r"(>?)<([^>]+)>", html)  # capture tags and angle brackets
    chunks = []
    for i in range(0, len(parts), 3):
        tag_part = parts[i + 1] if i + 1 < len(parts) else ""
        text = parts[i] if i < len(parts) else ""
        # Determine if this segment is a tag
        is_tag = bool(tag_part)
        chunks.append((text, is_tag))
    return chunks


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def translate_markup(source: str, target_lang: str = "en") -> str:
    """Translate HTML/markup text, preserving markup tags.

    Parameters:
        source: string containing HTML or any markup.
        target_lang: ISO language code of destination.
    Returns:
        Translated string with original tags intact.
    """
    client = build_client()
    # Identify text nodes and tags
    chunks = _split_markup(source)
    translated_parts = []
    for text, is_tag in chunks:
        if is_tag:
            # Keep tag unchanged
            translated_parts.append(text)
        else:
            # Translate only the plain text node
            raw_resp = client.translate(text, target_language=target_lang)
            translated_text = parse_translate_text_response(raw_resp)
            translated_parts.append(translated_text)
    return "".join(translated_parts)


# Helper for unit tests / demos
if __name__ == "__main__":
    demo_html = "<p>Hello <b>world</b>!</p>"
    print("Original:", demo_html)
    print("Translated:", translate_markup(demo_html, target_lang="es"))
