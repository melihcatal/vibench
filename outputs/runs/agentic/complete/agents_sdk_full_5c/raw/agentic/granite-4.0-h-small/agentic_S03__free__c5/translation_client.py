# General Text Translation client utilities

import os
from google.cloud import translate_v2 as translate

class TranslationClient:
    """Thin wrapper around Google Cloud Translation API client.

    Provider identifiable by `google.cloud.translate_v2` import and use of
    os.getenv('GOOGLE_APPLICATION_CREDENTIALS').
    """
    def __init__(self):
        self.client = translate.Client()

    def translate(self, text, source_language='en', target_language='es'):
        """Send a translate request to the API and return raw response."""
        return self.client.translate(text, source_language=source_language, target_language=target_language)

    @classmethod
    def from_env(cls):
        """Create a client using credentials from environment variables."""
        return cls()
