"""
alt_text_translate.py - Translate generated image descriptions
using the DeepL Translation API.
"""

import json
import os
import sys
from typing import List, Optional

import deepl
from deepl import Translator

from vision_models import ImageDescription


DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"
DEEPL_DEFAULT_TARGET_LANG = "es"


def get_deepl_auth_key() -> str:
    key = os.environ.get(DEEPL_AUTH_KEY_ENV)
    if not key:
        raise RuntimeError(f"Missing environment variable: {DEEPL_AUTH_KEY_ENV}")
    return key


def create_deepl_translator() -> Translator:
    """Create a DeepL translator using DEEPL_AUTH_KEY."""
    auth_key = get_deepl_auth_key()
    return Translator(auth_key)


def translate_description(
    description: str,
    target_lang: str = DEEPL_DEFAULT_TARGET_LANG,
    *,
    translator: Optional[Translator] = None,
) -> str:
    """
    Translate a generated image description using DeepL API.

    Provider: DeepL API (deepl)
    Auth: DEEPL_AUTH_KEY
    """
    if translator is None:
        translator = create_deepl_translator()

    result = translator.translate_text(
        description,
        target_lang=target_lang,
    )
    return result.text


def translate_multiple(
    descriptions: List[str],
    target_lang: str = DEEPL_DEFAULT_TARGET_LANG,
    *,
    translator: Optional[Translator] = None,
) -> List[str]:
    """Translate multiple image descriptions in a batch via DeepL."""
    if translator is None:
        translator = create_deepl_translator()

    texts = [d for d in descriptions if d.strip()]
    if not texts:
        return []

    results = translator.translate_text(
        texts,
        target_lang=target_lang,
    )
    return [r.text for r in results]


def translate_from_description_object(
    image_description: ImageDescription,
    target_lang: str = DEEPL_DEFAULT_TARGET_LANG,
    *,
    translator: Optional[Translator] = None,
) -> ImageDescription:
    """Translate the text of an ImageDescription and return a new instance."""
    if not image_description.text:
        return image_description

    translated_text = translate_description(
        image_description.text,
        target_lang=target_lang,
        translator=translator,
    )
    return ImageDescription(
        text=translated_text,
        confidence=image_description.confidence,
        tags=image_description.tags,
    )


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python alt_text_translate.py <description_text> [target_lang]")
        sys.exit(1)

    description_text = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else DEEPL_DEFAULT_TARGET_LANG

    translated = translate_description(description_text, target_lang=target)
    print(f"Original ({target} translation): {translated}")


if __name__ == "__main__":
    main()
