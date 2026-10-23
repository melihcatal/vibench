import os
from typing import Optional

import deepl

def alt_text_translate(caption: str, target_lang: str = &quot;ES&quot;) -&gt; str:
    auth_key = os.getenv(&quot;DEEPL_AUTH_KEY&quot;)
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(caption, target_lang=target_lang)
    return result.text