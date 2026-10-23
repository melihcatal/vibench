import os
from google.cloud import translate_v3 as translate

def get_translation_client():
    client = translate.TranslationServiceClient()
    return client

def location_path(project_id, location):
    return translate.TranslationServiceClient.location_path(project_id, location)