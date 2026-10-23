from google.cloud import vision
from google.cloud import translate_v3
from google.cloud import language_v1
from google.cloud import storage
import os

def get_vision_client():
    return vision.ImageAnnotatorClient()

def get_translate_client():
    return translate_v3.TranslationServiceClient()

def get_language_client():
    return language_v1.LanguageServiceClient()

def get_storage_client():
    return storage.Client()
