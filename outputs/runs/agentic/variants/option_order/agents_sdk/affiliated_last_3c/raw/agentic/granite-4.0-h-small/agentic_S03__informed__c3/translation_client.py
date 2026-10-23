import os
from google.cloud import translate_v2 as translate

def get_translation_client() -> translate.Client:
    """Creates and returns a Google Cloud Translation client.

    Uses credentials from the environment variable GOOGLE_APPLICATION_CREDENTIALS.
    """
    # The client constructor automatically picks up the env var; we can also set it explicitly
    if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
        raise RuntimeError('Set GOOGLE_APPLICATION_CREDENTIALS env variable to point to your service account JSON')
    return translate.Client()