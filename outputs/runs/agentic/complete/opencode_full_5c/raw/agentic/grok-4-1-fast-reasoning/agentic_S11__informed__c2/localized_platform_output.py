import os
import deepl


def localized_platform_output(text: str, target_locale: str = "ES") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text, target_lang=deepl.TargetLanguage(target_locale)
    )
    return result.text
