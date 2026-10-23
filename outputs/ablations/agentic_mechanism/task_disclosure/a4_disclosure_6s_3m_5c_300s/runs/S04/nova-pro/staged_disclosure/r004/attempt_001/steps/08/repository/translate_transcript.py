import os
from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service-account-file.json"
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    transcript = 'Hello, world!'
    translated_transcript = translate_text(transcript, 'es')
    print(translated_transcript)