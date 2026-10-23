from translation_client import get_translator, get_target_lang_code
from translation_models import normalize_text


def translate_markup(markup: str, source_language: str, target_language: str) -> str:
    return str(
        get_translator().translate_text(
            normalize_text(markup),
            source_lang=normalize_text(source_language),
            target_lang=get_target_lang_code(normalize_text(target_language)),
            preserve_formatting=True,
        )
    )
