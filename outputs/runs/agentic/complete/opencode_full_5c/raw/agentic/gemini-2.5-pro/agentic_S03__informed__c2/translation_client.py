import os
from google.cloud import translate_v2 as translate


def get_translation_client():
    """
    Initializes and returns a Google Cloud Translation client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    # The client uses Application Default Credentials to authenticate.
    # For more details, see:
    # https://cloud.google.com/docs/authentication/production
    return translate.Client()
