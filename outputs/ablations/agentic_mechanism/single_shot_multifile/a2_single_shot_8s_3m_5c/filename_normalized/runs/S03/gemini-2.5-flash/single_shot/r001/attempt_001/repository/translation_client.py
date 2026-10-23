import os
from google.cloud import translate_v3

_translation_client = None

def get_translation_client():
    global _translation_client
    if _translation_client is None:
        _translation_client = translate_v3.TranslationServiceClient()
    return _translation_client
