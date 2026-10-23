import os
from google.cloud import language_v1

def get_safety_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = language_v1.LanguageServiceClient()
    return client