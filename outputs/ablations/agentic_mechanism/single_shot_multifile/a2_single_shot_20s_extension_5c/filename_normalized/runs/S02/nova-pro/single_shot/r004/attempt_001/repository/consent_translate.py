from deep_translator import GoogleTranslator

def translate_consent(text, target_language='es'):
    translator = GoogleTranslator(source='auto', target=target_language)
    translated_text = translator.translate(text)
    return translated_text

if __name__ == '__main__':
    print(translate_consent('your consent text here'))