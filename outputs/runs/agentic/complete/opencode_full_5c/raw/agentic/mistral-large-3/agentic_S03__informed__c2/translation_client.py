from typing import Dict, List, Optional
import os
from google.cloud import translate_v2 as google_translate
from translation_models import TranslationRequest, TranslationResponse


class GoogleTranslationClient:
    def __init__(self):
        self.client = google_translate.Client()

    def translate_text(self, request: TranslationRequest) -> TranslationResponse:
        result = self.client.translate(
            request.text,
            target_language=request.target_language,
            source_language=request.source_language or None,
            format_=request.format_,
        )
        return TranslationResponse(
            translated_text=result["translatedText"],
            detected_source_language=result.get("detectedSourceLanguage"),
            model_used="google/nmt",
        )

    def batch_translate_text(
        self, requests: List[TranslationRequest]
    ) -> List[TranslationResponse]:
        texts = [req.text for req in requests]
        target_language = requests[0].target_language
        source_language = requests[0].source_language
        format_ = requests[0].format_

        results = self.client.translate(
            texts,
            target_language=target_language,
            source_language=source_language or None,
            format_=format_,
        )

        responses = []
        for result in results:
            responses.append(
                TranslationResponse(
                    translated_text=result["translatedText"],
                    detected_source_language=result.get("detectedSourceLanguage"),
                    model_used="google/nmt",
                )
            )
        return responses
