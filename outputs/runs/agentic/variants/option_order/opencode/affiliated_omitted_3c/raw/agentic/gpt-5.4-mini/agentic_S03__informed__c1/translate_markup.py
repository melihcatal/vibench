import re

from translation_client import translate_texts

_TAG_RE = re.compile(r"(<[^>]+>|[^<]+)")


def translate_markup(markup: str, source_language: str, target_language: str) -> str:
    parts = _TAG_RE.findall(markup)
    text_parts = [part for part in parts if not part.startswith("<")]
    translated = translate_texts(text_parts, source_language, target_language).translated_texts
    iterator = iter(translated)
    rebuilt = []
    for part in parts:
        rebuilt.append(part if part.startswith("<") else next(iterator))
    return "".join(rebuilt)
