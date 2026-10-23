import os
from google.cloud import translate

client = translate.TranslationServiceClient()

def translate(text, target_language_code):
    parent = f'projects/{os.getenv(