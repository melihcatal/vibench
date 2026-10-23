from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    text_to_translate = 'Enter appeal text here'
    target_language = 'en'
    translated_text = translate_text(text_to_translate, target_language)
    print(f'Translated text: {translated_text}')
