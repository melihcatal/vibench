import os
from deepl import Translator
from model_models import TranslationResult


def localized_platform_output(text: str, target_locale: str) -> TranslationResult:
    translator = Translator(os.environ["DEEPL_AUTH_KEY"])
    response = translator.translate_text(text, target_lang=target_locale.upper())
    return TranslationResult(
        text=response.text,
        target_locale=target_locale,
        detected_language=getattr(response, "detected_source_lang", None),
        raw_response=response,
    )
