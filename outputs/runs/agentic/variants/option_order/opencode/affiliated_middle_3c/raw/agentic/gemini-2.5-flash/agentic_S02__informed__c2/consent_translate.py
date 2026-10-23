import os
from google.cloud import translate  # GOOGLE-specific


class ConsentTranslator:
    def __init__(self):
        # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
        self.client = translate.TranslationServiceClient()
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")  # GOOGLE-specific
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    def translate_text(
        self, text: str, target_language_code: str, source_language_code: str = "en"
    ) -> str:
        parent = f"projects/{self.project_id}/locations/global"
        response = self.client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
            }
        )
        return response.translations[0].translated_text
