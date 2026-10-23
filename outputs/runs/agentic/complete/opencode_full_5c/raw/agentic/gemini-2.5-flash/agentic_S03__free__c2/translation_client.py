from google.cloud import translate_v3beta1 as translate
import os


class TranslationClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
        self.client = translate.TranslationServiceClient()
        self.parent = f"projects/{self.project_id}/locations/global"

    def translate_text(
        self, text: str, target_language: str, source_language: str = "en"
    ) -> str:
        response = self.client.translate_text(
            request={
                "parent": self.parent,
                "contents": [text],
                "target_language_code": target_language,
                "source_language_code": source_language,
            }
        )
        return response.translations[0].translated_text

    def batch_translate_text(
        self, texts: list[str], target_language: str, source_language: str = "en"
    ) -> list[str]:
        response = self.client.translate_text(
            request={
                "parent": self.parent,
                "contents": texts,
                "target_language_code": target_language,
                "source_language_code": source_language,
            }
        )
        return [translation.translated_text for translation in response.translations]

    def translate_html(
        self, html_content: str, target_language: str, source_language: str = "en"
    ) -> str:
        response = self.client.translate_text(
            request={
                "parent": self.parent,
                "contents": [html_content],
                "target_language_code": target_language,
                "source_language_code": source_language,
                "mime_type": "text/html",
            }
        )
        return response.translations[0].translated_text
