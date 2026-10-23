import os
from google.cloud import translate_v2 as translate

def get_translation_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'
    return translate.Client()