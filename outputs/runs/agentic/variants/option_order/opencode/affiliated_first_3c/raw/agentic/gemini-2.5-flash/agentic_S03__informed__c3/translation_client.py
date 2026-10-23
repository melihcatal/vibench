import os
from google.cloud import translate_v2 as translate
from translation_models import TranslationRequest, TranslationResponse


class GoogleTranslationClient:
    def __init__(self):
        # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
        self.client = translate.Client()

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        if isinstance(request.text, list):
            results = self.client.translate(
                request.text,
                target_language=request.target_language,
                source_language=request.source_language,
                format_=request.format,
            )
            translated_texts = [result["translatedText"] for result in results]
            detected_source_languages = [
                result["detectedSourceLanguage"] for result in results
            ]
            return TranslationResponse(translated_texts, detected_source_languages)
        else:
            result = self.client.translate(
                request.text,
                target_language=request.target_language,
                source_language=request.source_language,
                format_=request.format,
            )
            return TranslationResponse(
                result["translatedText"], result.get("detectedSourceLanguage")
            )
