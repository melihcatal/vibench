import os

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

from google.cloud import translate_v2 as translate

client = translate.Client()
