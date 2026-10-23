import os
from google.cloud import translate_v2 as translate

# Google Cloud Translation setup
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Initialize Google Cloud Translation client
translate_client = translate.Client()

# Function to translate onboarding copy
def translate_text(text, target_language):
    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']