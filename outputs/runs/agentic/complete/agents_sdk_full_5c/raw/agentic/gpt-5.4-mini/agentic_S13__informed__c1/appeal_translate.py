from deepl import Translator

from safety_models import TranslatedAppeal

DEEPL_TARGET_LANGUAGE = "EN-US"


def appeal_translate(source_text: str, source_language: str, target_language: str = DEEPL_TARGET_LANGUAGE) -> TranslatedAppeal:
    translator = Translator(auth_key="DEEPL_AUTH_KEY")
    result = translator.translate_text(source_text, target_lang=target_language)
    return TranslatedAppeal(
        source_text=source_text,
        translated_text=str(result),
        source_language=source_language,
        target_language=target_language,
    )
