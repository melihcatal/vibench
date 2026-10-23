import os
from google.cloud import translate_v3 as translate

class TranslationClient:
    def __init__(self):
        self.client = translate.TranslationServiceClient()
        self.parent = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}/locations/global"

    def translate_text(self, text, target_language, source_language=None):
        response = self.client.translate_text(
            parent=self.parent,
            contents=[text],
            mime_type="text/plain",
            target_language_code=target_language,
            source_language_code=source_language
        )
        return response.translations[0].translated_text

    def batch_translate(self, texts, target_language, source_language=None):
        response = self.client.translate_text(
            parent=self.parent,
            contents=texts,
            mime_type="text/plain",
            target_language_code=target_language,
            source_language_code=source_language
        )
        return [translation.translated_text for translation in response.translations]