from google.cloud import translate_v2 as translate

def translate_text(text, target_language='en'):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    consent_text = 'Sample consent text to be translated.'
    translated_text = translate_text(consent_text)
    print(f'Translated text: {translated_text}')
