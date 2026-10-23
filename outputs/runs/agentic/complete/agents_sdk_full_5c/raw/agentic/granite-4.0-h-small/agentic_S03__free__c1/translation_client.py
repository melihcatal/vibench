# [HELPER] translation_client.py
import os
from google.cloud import translate_v2 as translate

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if not GOOGLE_APPLICATION_CREDENTIALS:
    raise RuntimeError('Set GOOGLE_APPLICATION_CREDENTIALS environment variable to path of service account JSON')

translate_client = translate.Client()

def get_client() -> translate.Client:
    return translate_client
