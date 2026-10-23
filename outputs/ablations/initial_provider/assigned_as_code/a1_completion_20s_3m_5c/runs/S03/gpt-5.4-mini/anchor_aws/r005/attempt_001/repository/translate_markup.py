import re

from translation_client import translation_client
from translation_models import escape_markup_text, normalize_language_code


TAG_RE = re.compile(r"(<[^>]+>)")


def translate_markup(payload, config=None):
    config = config or {}
    client = translation_client(config)
    parts = TAG_RE.split(payload.get("markup", ""))
    translated_parts = []
    for part in parts:
        if part.startswith("<") and part.endswith(">"):
            translated_parts.append(part)
        elif part:
            response = client.translate_text(
                Text=escape_markup_text(part),
                SourceLanguageCode=normalize_language_code(payload.get("source_language")),
                TargetLanguageCode=normalize_language_code(payload.get("target_language")),
            )
            translated_parts.append(response["TranslatedText"])
    return {
        "markup": "".join(translated_parts),
        "source_language": payload.get("source_language"),
        "target_language": payload.get("target_language"),
    }
