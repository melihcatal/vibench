from google.cloud import translate_v3
import os

class TranslationClient:
    def __init__(self, project_id: str = None):
        self.client = translate_v3.TranslationServiceClient()
        self.project_id = project_id if project_id else os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")
        self.parent = f"projects/{self.project_id}"

    def translate_text(self, text: str, target_language_code: str, source_language_code: str = None) -> str:
        request = {
            "parent": self.parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
        if source_language_code:
            request["source_language_code"] = source_language_code

        response = self.client.translate_text(request=request)
        return response.translations[0].translated_text
