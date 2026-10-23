from dataclasses import dataclass
import os

from google.cloud import translate_v3 as translate

@dataclass
class TranslateTextRequest:
    text: str
    source_language_code: str
    target_language_code: str

@dataclass
class TranslateTextResponse:
    translated_text: str
    detected_language_code: str

class TranslationClient:
    def __init__(self):
        self.client = translate.TranslationServiceClient()
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
        self.parent = f"projects/{self.project_id}/locations/global"

    def translate_text(self, request: TranslateTextRequest) -> TranslateTextResponse:
        response = self.client.translate_text(
            request=translate.TranslateTextRequest(
                parent=self.parent,
                contents=[request.text],
                source_language_code=request.source_language_code,
                target_language_code=request.target_language_code,
            )
        )
        translation = response.translations[0]
        return TranslateTextResponse(
            translated_text=translation.translated_text,
            detected_language_code=translation.detected_language_code
        )
