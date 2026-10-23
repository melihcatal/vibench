
import os
from google.cloud import translate_v2 as translate

class TranslationClient:
    def __init__(self):
        # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
        # with the path to your service account key file.
        # Alternatively, you can explicitly pass credentials:
        # from google.oauth2 import service_account
        # credentials = service_account.Credentials.from_service_account_file(
        #     'path/to/your/key.json')
        # self.client = translate.Client(credentials=credentials)
        self.client = translate.Client()

    def translate_text(self, text, target_language='en', source_language=None):
        """Translates text into the target language.

        Args:
            text: The text to translate.
            target_language: The language to translate the text into (e.g., 'en', 'es', 'fr').
            source_language: The language of the input text (optional).

        Returns:
            A dictionary containing the translated text, detected source language,
            and model used.
        """
        if source_language:
            result = self.client.translate(
                text,
                target_language=target_language,
                source_language=source_language
            )
        else:
            result = self.client.translate(
                text,
                target_language=target_language
            )

        return result

