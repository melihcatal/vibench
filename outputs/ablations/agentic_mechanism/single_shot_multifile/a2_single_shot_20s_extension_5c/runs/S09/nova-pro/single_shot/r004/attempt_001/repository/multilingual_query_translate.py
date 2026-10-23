import os
import google.auth
from google.cloud import translate_v2 as translate

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your-google-cloud-keyfile.json'
translate_client = translate.Client()

def translate_query(query, target_language):
    translation = translate_client.translate(query, target_language=target_language)
    return translation['translatedText']