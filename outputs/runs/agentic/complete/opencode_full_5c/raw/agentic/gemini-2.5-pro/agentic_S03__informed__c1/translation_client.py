import os
from google.cloud import translate_v2 as translate


def get_translation_client():
    """
    Initializes and returns a Google Cloud Translation client.

    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise EnvironmentError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable not set."
        )
    return translate.Client()
