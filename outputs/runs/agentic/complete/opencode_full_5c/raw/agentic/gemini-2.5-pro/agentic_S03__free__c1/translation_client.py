import os
from google.cloud import translate_v2 as translate


def get_translation_client():
    """
    Initializes and returns a Google Cloud Translation client.
    Assumes that the GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise EnvironmentError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable not set."
        )
    return translate.Client()
