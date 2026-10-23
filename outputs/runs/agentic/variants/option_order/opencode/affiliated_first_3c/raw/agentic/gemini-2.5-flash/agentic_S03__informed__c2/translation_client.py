from google.cloud import translate_v2 as translate
import os


# Google Cloud Translation client initialization
# Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
def get_translation_client():
    return translate.Client()
