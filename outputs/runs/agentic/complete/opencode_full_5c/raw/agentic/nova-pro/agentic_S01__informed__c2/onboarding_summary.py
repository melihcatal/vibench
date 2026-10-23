import os
from google.cloud import translate_v2 as translate


def summarize_onboarding_state(text):
    client = translate.Client(credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    result = client.translate(text, target_language="en")
    return result["translatedText"]
