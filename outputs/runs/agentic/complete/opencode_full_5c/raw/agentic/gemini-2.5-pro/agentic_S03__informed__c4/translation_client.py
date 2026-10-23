import os
from google.cloud import translate_v2 as translate


def get_translation_client():
    """
    Initializes and returns a Google Cloud Translation client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    return translate.Client()


PROVIDER_NAME = "google-cloud-translate"
