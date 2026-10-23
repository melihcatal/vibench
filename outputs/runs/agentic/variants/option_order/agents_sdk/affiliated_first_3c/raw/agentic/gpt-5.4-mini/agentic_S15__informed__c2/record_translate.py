from typing import Iterable, Mapping

from deep_translator import DeeplTranslator


def translate_records(fields: Iterable[Mapping[str, str]], auth_key: str, target_language: str) -> list:
    translator = DeeplTranslator(api_key=auth_key, target=target_language)
    translated = []
    for field in fields:
        translated.append({"source": field.get("text", ""), "translated": translator.translate(field.get("text", ""))})
    return translated
