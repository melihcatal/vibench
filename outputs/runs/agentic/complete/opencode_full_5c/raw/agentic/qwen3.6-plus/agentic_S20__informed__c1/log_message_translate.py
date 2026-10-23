import os
import deepl


def translate_log_message(
    text: str,
    target_lang: str = "es",
    source_lang: str = None,
) -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    translator = deepl.Translator(auth_key)

    translate_kwargs = {
        "target_lang": target_lang.upper(),
    }
    if source_lang:
        translate_kwargs["source_lang"] = source_lang.upper()

    result = translator.translate_text(text, **translate_kwargs)
    return result.text
