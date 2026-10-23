from dataclasses import dataclass
import os

from google.cloud import translate_v3 as translate

@dataclass
class BatchTranslateRequest:
    texts: list[str]
    source_language_code: str
    target_language_code: str

@dataclass
class BatchTranslateResponse:
    translations: list[str]
    detected_language_codes: list[str]

class TranslationClient:
    def __init__(self):
        self.client = translate.TranslationServiceClient()
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
        self.parent = f"projects/{self.project_id}/locations/global"

    def batch_translate_text(self, request: BatchTranslateRequest) -> BatchTranslateResponse:
        response = self.client.translate_text(
            request=translate.TranslateTextRequest(
                parent=self.parent,
                contents=request.texts,
                source_language_code=request.source_language_code,
                target_language_code=request.target_language_code,
            )
        )
        translated_texts = [t.translated_text for t in response.translations]
        detected_languages = [t.detected_language_code for t in response.translations]
        return BatchTranslateResponse(
            translations=translated_texts,
            detected_language_codes=detected_languages
        )
