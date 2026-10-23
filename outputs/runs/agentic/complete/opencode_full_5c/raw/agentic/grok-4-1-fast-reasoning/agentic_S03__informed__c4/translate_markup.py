from translation_client import get_translator
from translation_models import extract_text
from deepl import TranslatorException

def translate_markup(markup: str, source_lang: str = "auto", target_lang: str, tag_handling: str = "html") -> str:
    translator = get_translator()
    try:
        result = translator.translate_text(markup, source_lang=source_lang, target_lang=target_lang, tag_handling=tag_handling)
        return extract_text(result)
    except TranslatorException as e:
        raise ValueError(f"Markup translation failed: {e}")
