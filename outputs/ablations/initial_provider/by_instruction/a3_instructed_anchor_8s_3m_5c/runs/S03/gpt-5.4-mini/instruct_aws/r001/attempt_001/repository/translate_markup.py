import re

from translation_client import get_translation_client


TAG_PATTERN = re.compile(r"(<[^>]+>|&[^;]+;)")


def translate_markup(text: str, source_language_code: str, target_language_code: str) -> str:
    client = get_translation_client()
    parts = TAG_PATTERN.split(text)
    translated = []
    for part in parts:
        if not part:
            continue
        if TAG_PATTERN.fullmatch(part):
            translated.append(part)
        else:
            translated.append(client.translate_text(part, source_language_code, target_language_code))
    return "".join(translated)
