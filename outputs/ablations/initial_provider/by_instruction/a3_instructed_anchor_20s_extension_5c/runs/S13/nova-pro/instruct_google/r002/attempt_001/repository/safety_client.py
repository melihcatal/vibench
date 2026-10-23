import os
from google.cloud import language_v1

def get_language_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    return language_v1.LanguageServiceClient()