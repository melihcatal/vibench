import os
import deepl
from model_models import TranslationResult

def translate_with_deepl(text: str, target_lang: str, source_lang: str = "auto") -> TranslationResult:
    auth_key = os.getenv("DEEPL_AUTH_KEY")

    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)

    return TranslationResult(
        translated_text=result.text,
        source_language=result.detected_source_lang,
        target_language=target_lang,
        raw_response={"detected_source_lang": result.detected_source_lang}
    )
