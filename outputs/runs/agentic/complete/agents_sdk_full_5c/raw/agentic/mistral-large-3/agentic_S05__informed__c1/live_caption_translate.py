import os
from google.cloud import translate_v2 as translate
from speech_models import TranslationRequest, TranslationResponse

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

class LiveCaptionTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        result = self.client.translate(
            request.text,
            target_language=request.target_language
        )
        return TranslationResponse(translated_text=result["translatedText"])