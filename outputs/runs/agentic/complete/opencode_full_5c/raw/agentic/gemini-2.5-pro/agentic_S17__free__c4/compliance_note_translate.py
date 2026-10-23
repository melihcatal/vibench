import os
from google.cloud import translate_v2 as translate


def translate_compliance_note(text: str, target_language: str) -> str:
    os.environ.setdefault(
        "GOOGLE_APPLICATION_CREDENTIALS",
        os.path.expanduser("~/.config/gcloud/application_default_credentials.json"),
    )

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
