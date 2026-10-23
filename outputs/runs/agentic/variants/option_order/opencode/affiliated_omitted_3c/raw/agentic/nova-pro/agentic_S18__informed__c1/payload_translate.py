import os
from google.cloud import translate_v2 as translate

# Set up the Translation client
client = translate.Client()


def payload_translate(text):
    # Translate customer-facing message payload text
    result = client.translate(text, target_language="en")
    return result["translatedText"]
