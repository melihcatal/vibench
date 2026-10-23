import os
from google.cloud import translate_v2 as translate

# Configuration
translate_client = translate.Client()


# Translate identity-provider consent copy
def translate_consent(text, target_language):
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
