from typing import Iterable, List

from translation_client import get_target_language_code, get_translator


def batch_translate(
    texts: Iterable[str], source_language: str, target_language: str
) -> List[str]:
    translator = get_translator()
    return [
        str(
            translator.translate_text(
                text,
                source_lang=source_language,
                target_lang=get_target_language_code(target_language),
            ).text
        )
        for text in texts
    ]
