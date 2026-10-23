import os
from google.cloud import translate_v3beta1 as translate

class TranslationClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
        self.client = translate.TranslationServiceClient()

    def translate_text(self, text, target_language_code, source_language_code=None):
        parent = f"projects/{self.project_id}"
        
        config = {
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
        
        response = self.client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
                "model": "projects/project-number/locations/global/models/general/nmt", # General purpose model
                "target_language_code": target_language_code,
            }
        )

        translated_text = ""
        for translation in response.translations:
            translated_text += translation.translated_text
        return translated_text

