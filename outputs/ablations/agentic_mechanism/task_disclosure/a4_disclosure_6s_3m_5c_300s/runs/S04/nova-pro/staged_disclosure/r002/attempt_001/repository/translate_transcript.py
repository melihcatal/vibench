import os
from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    transcript_segment = 'Hello, world!'
    target_language = 'es'
    translated_segment = translate_text(transcript_segment, target_language)
    print(f'Translated segment: {translated_segment}')
