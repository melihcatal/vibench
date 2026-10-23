import os
from google.cloud import translate_v2 as translate

def appeal_translate(text, target_language='es'):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    text = 'Your appeal text here'
    translated_text = appeal_translate(text)
    print(f'Translated Text: {translated_text}')
