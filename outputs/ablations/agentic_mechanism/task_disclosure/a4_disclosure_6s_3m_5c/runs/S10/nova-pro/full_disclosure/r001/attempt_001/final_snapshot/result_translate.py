import os

from google.cloud import translate_v3beta1 as translate


def translate_text(text, target_language='en'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = translate.TranslationServiceClient()
    parent = client.location_path('my-project-id', 'global')
    response = client.translate_text(parent=parent, contents=[text], target_language_code=target_language)
    translations = [translation.translated_text for translation in response.translations]
    return translations[0]


if __name__ == '__main__':
    sample_text = 'Hello, world!'
    translated_text = translate_text(sample_text)
    print(f'Translated text: {translated_text}')
