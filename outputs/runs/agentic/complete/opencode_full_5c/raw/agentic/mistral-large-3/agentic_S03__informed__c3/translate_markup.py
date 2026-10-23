from typing import Optional
import re
from translation_client import DeepLTranslationClient
from translation_models import TranslationRequest


def translate_markup(
    markup: str, target_language: str, source_language: Optional[str] = None
) -> str:
    """
    Translates HTML or markup while preserving tags using DeepL API.
    """
    tag_pattern = re.compile(r"<[^>]+>|[^<]+")
    parts = tag_pattern.findall(markup)
    translated_parts = []

    client = DeepLTranslationClient()

    for part in parts:
        if part.startswith("<"):
            translated_parts.append(part)
        else:
            request = TranslationRequest(
                text=part.strip(),
                target_language=target_language,
                source_language=source_language,
            )
            response = client.translate_text(request)
            translated_parts.append(response.translated_text)

    return "".join(translated_parts)
