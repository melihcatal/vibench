import os
from google.cloud import translate_v2 as translate

def get_translation_client():
    return translate.Client()