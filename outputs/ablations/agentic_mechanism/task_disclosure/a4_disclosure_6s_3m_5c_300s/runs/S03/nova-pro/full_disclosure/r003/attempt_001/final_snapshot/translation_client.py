import os
from google.cloud import translate_v2 as translate

# Configuration
PROJECT_ID = 'your-project-id'

# Client helper utilities
def get_translate_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your-service-account-file.json'
    return translate.Client()

def translate_text(client, text, target_language):
    return client.translate(text, target_language=target_language)