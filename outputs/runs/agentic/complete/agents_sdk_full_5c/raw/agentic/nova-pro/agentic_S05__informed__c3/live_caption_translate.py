from deepl import Translator

# Translate live captions into another language

def translate_caption(text, target_lang='ES'):
    translator = Translator(auth_key='your-deepl-auth-key')
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text