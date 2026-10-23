&quot;&quot;&quot;
Translates identity-provider consent copy using DeepL API.
&quot;&quot;&quot;
import os
import deepl
from typing import Optional

translator = deepl.Translator(os.getenv(&#x27;DEEPL_AUTH_KEY&#x27;))

def translate_consent(text: str, target_lang: str = &quot;ES&quot;, source_lang: Optional[str] = None) -&gt; str:
    &quot;&quot;&quot;
    Translates consent text to target language.
    &quot;&quot;&quot;
    result = translator.translate_text(
        text,
        target_lang=target_lang,
        source_lang=source_lang
    )
    return result.text