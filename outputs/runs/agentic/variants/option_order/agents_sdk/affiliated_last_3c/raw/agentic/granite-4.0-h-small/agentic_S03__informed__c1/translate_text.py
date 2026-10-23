import os
from google.cloud import translate_v2 as translate

def translate_text(source_text, target_language='es'):
    # Initializes the Google Cloud Translation client (uses env var GOOGLE_APPLICATION_CREDENTIALS)
    client = translate.Client()
    result = client.translate(source_text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    text = "Hello, world!"
    print(translate_text(text, 'fr'))