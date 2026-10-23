import os
from google.cloud import translate_v2 as translate

def translate_live_captions(captions, target_language):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/google-cloud-credentials.json'
    translate_client = translate.Client()
    translated_captions = []
    for caption in captions:
        translation = translate_client.translate(caption, target_language=target_language)
        translated_captions.append(translation['translatedText'])
    return translated_captions

if __name__ == '__main__':
    live_captions = ['Hello, world!', 'This is a test caption.']
    target_language = 'es'
    translated_captions = translate_live_captions(live_captions, target_language)
    print(translated_captions)