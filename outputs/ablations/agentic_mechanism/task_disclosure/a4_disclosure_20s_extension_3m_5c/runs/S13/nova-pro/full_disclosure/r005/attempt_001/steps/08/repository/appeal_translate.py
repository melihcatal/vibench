from google.cloud import translate_v2 as translate

def translate_text(text, target_language='en'):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    appeal_text = 'Sample appeal text to be translated.'
    translated_text = translate_text(appeal_text)
    print(f'Translated text: {translated_text}')
