from deepl import Translator

def translate_markup(text, target_language):
    translator = Translator(auth_key="<your-deepl-auth-key>")
    result = translator.translate_text(text, target_lang=target_language, preserve_formatting=True)
    return result.text