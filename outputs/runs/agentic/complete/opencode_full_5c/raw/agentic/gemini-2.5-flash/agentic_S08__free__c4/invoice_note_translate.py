import os
from google.cloud import translate_v3 as translate


class InvoiceNoteTranslator:
    def __init__(self):
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        if not project_id:
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT_ID environment variable not set for Translation API."
            )
        self.project_id = project_id
        self.client = translate.TranslationServiceClient()
        self.parent = f"projects/{self.project_id}/locations/global"

    def translate_text(self, text: str, target_language_code: str = "en") -> str:
        if not text:
            return ""

        response = self.client.translate_text(
            request={
                "parent": self.parent,
                "contents": [text],
                "target_language_code": target_language_code,
            }
        )

        if response.translations:
            return response.translations[0].translated_text
        return ""
