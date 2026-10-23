import os
from typing import Optional
from google.cloud import translate_v2 as translate
from translation_models import TranslationRequest, TranslationResponse

class TextTranslator:
    def __init__(self):
        self.client = translate.Client.from_service_account_json(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
        )

    def translate_text(
        self, 
        text: str, 
        target_language: str, 
        source_language: Optional[str] = None,
        model: str = "nmt"
    ) -> TranslationResponse:
        result = self.client.translate(
            text,
            target_language=target_language,
            source_language=source_language,
            model=model
        )
        return TranslationResponse(
            translated_text=result["translatedText"],
            detected_source_language=result.get("detectedSourceLanguage"),
            model_used=result.get("model")
        )

def translate_text(request: TranslationRequest) -> TranslationResponse:
    translator = TextTranslator()
    return translator.translate_text(
        text=request.text,
        target_language=request.target_language,
        source_language=request.source_language
    )