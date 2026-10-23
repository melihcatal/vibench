import os
from google.cloud import translate_v2 as translate


def moderation_summary(decisions):
    client = translate.Client(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    summary = " ".join([str(decision) for decision in decisions])
    result = client.translate(summary, target_language="en")
    return result["translatedText"]
