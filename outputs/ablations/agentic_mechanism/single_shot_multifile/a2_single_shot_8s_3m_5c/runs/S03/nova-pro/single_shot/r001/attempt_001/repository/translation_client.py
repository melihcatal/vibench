import os
from google.cloud import translate_v2 as translate

def get_translate_client():
    return translate.Client(key=os.getenv('GOOGLE_CLOUD_TRANSLATE_API_KEY'))