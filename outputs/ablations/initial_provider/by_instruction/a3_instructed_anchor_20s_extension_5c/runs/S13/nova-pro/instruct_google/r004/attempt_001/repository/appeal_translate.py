import os
from google.cloud import translate_v2 as translate

def translate_appeal_text(text, target_language='en'):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    sample_text = 'This is an appeal text to translate.'
    translated_text = translate_appeal_text(sample_text)
    print(f'Translated text: {translated_text}')
