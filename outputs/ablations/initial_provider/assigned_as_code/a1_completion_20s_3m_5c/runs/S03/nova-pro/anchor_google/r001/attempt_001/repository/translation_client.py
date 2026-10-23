import os
from google.cloud import translate_v3


def get_config():
    return {
        'project_id': os.getenv('GOOGLE_CLOUD_PROJECT_ID'),
        'location': os.getenv('GOOGLE_CLOUD_LOCATION', 'global'),
    }


def get_client(config):
    return translate_v3.TranslationServiceClient()