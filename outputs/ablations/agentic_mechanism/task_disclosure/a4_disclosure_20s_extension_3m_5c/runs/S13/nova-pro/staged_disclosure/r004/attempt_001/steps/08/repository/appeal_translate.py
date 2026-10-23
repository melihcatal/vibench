from google.cloud import translate_v2 as translate

def translate_text(text):
    client = translate.Client()
    result = client.translate(text, target_language='en')
    return result['translatedText']

if __name__ == '__main__':
    appeal_text = 'Enter appeal text here'
    translated_text = translate_text(appeal_text)
    print(f'Translated text: {translated_text}')
