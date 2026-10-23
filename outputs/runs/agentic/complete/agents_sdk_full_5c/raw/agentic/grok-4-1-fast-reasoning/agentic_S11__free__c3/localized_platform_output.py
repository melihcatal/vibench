import os
import deepl

def localized_platform_output(output: str, target_locale: str = "FR") -> str:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(output, target_lang=target_locale)
    return result.text
