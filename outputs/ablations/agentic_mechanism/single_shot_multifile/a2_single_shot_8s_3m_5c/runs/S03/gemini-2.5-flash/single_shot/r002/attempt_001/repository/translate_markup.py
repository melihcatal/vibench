from dataclasses import dataclass
import os

from google.cloud import translate_v3 as translate

@dataclass
class TranslateMarkupRequest:
    markup_text: str
    source_language_code: str
    target_language_code: str
    mime_type: str = "text/html"

@dataclass
class TranslateMarkupResponse:
    translated_markup: str
    detected_language_code: str

class TranslationClient:
    def __init__(self):
        self.client = translate.TranslationServiceClient()
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
        self.parent = f"projects/{self.project_id}/locations/global"

    def translate_markup(self, request: TranslateMarkupRequest) -> TranslateMarkupResponse:
        response = self.client.translate_text(
            request=translate.TranslateTextRequest(
                parent=self.parent,
                contents=[request.markup_text],
                source_language_code=request.source_language_code,
                target_language_code=request.target_language_code,
                mime_type=request.mime_type,
            )
        )
        translation = response.translations[0]
        return TranslateMarkupResponse(
            translated_markup=translation.translated_text,
            detected_language_code=translation.detected_language_code
        )
