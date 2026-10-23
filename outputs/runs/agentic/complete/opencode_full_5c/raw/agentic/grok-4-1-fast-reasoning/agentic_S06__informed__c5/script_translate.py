import os
import deepl


def translate_script(script: str, target_lang: str = "EN") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        script, target_lang=deepl.TargetLanguage(target_lang)
    )
    return result.text
