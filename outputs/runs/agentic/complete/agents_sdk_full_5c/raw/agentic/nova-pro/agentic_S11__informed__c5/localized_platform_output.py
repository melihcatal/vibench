from deepl import Translator

def translate_text(text):
    translator = Translator(auth_key='your-deepl-auth-key')
    result = translator.translate_text(text, target_lang='DE')
    print(result.text)