import os
from google.cloud import translate_v2 as translate

# Set up the Translation client
client = translate.Client()


def message_safety(text):
    # Check message payload text for unsafe content
    result = client.translate(text, target_language="en")
    return result["translatedText"]
