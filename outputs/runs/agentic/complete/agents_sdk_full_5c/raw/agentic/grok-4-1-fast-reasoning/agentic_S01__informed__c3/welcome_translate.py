import os
import deepl

def translate_onboarding_copy(text: str, target_locale: str) -&gt; str:
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_locale)
    return result.text