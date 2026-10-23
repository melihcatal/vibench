import deepl

# Set your DeepL API key here
DEEPL_API_KEY = 'your-deepl-api-key'

# Initialize the DeepL translator
translator = deepl.Translator(DEEPL_API_KEY)

def translate_appeal(text, target_lang='EN'):
    """Translate appeal text to the specified target language"""
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text

if __name__ == '__main__':
    appeal_text = 'Enter appeal text here'
    translated_text = translate_appeal(appeal_text)
    print(f'Translated text: {translated_text}')
