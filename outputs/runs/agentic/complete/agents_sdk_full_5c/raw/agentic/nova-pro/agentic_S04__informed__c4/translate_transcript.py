import os
from google.cloud import translate_v2 as translate

def translate_transcript(transcript, target_language='es'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = translate.Client()
    translation = client.translate(transcript, target_language=target_language)
    return translation['translatedText']