from deep_translator import GoogleTranslator

def record_translate(text, target_language='en'):
    translator = GoogleTranslator(source='auto', target=target_language)
    return translator.translate(text)