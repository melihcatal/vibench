import os
from deepl import Translator, TargetLanguage

translator = Translator(os.getenv("DEEPL_AUTH_KEY"))

def translate_consent(text: str, source_lang: str = "auto", target_lang: str = "EN-US"):
    result = translator.translate_text(
        text,
        source_lang=source_lang,
        target_lang=TargetLanguage(target_lang)
    )
    return result.text

# Provider-specific: deepl SDK, DeepL API