import os
from google.cloud import translate_v2 as translate


def get_translation_client():
    """
    Initializes and returns a Google Cloud Translation client.
    Assumes that GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    return translate.Client()
