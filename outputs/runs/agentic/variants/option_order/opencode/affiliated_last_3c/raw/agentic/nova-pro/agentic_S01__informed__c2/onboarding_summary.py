import os
from google.cloud import translate_v2 as translate

# Configuration
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

translate_client = translate.Client()


def onboarding_summary(text):
    result = translate_client.translate(text, target_language="en")
    return result["translatedText"]
