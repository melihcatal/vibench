import os
from google.cloud import translate_v2 as translate

# Set up the Translation client
client = translate.Client()


def message_summary(text):
    # Summarize the message processing results
    result = client.translate(text, target_language="en")
    return result["translatedText"]
