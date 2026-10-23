from deepl import Translator

def translate_message(message, target_lang):
    translator = Translator(os.getenv('DEEPL_AUTH_KEY'))
    result = translator.translate_text(message, target_lang=target_lang)
    return result.text

if __name__ == '__main__':
    translated = translate_message('Hello, world!', 'FR')
    print(translated)