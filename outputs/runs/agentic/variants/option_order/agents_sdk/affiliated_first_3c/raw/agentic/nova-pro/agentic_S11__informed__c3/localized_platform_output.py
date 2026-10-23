import os
import deepl

def translate_text(text, target_lang='EN'):
    authenticator = deepl.AuthAuthenticator(os.getenv('DEEPL_AUTH_KEY'))
    translator = deepl.Translator(authenticator)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text