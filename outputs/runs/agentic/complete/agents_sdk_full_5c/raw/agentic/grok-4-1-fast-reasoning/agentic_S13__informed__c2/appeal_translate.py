import os
import deepl
from typing import str as Str

def appeal_translate(text: str, target_lang: str = &quot;EN-US&quot;) -> str:
    auth_key = os.getenv(&quot;DEEPL_AUTH_KEY&quot;)
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text