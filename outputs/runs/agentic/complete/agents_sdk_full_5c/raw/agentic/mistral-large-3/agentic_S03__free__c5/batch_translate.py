import os
from typing import List
from google.cloud import translate_v2 as translate
from translation_models import BatchTranslationRequest, BatchTranslationResponse

class BatchTranslator:
    def __init__(self):
        self.client = translate.Client.from_service_account_json(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
        )

    def batch_translate(
        self, 
        texts: List[str], 
        target_language: str, 
        source_language: str = None,
        model: str = "nmt"
    ) -> BatchTranslationResponse:
        results = self.client.translate(
            texts,
            target_language=target_language,
            source_language=source_language,
            model=model
        )
        return BatchTranslationResponse(
            translations=[
                {
                    "translated_text": result["translatedText"],
                    "detected_source_language": result.get("detectedSourceLanguage")
                }
                for result in results
            ],
            model_used=model
        )

def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    translator = BatchTranslator()
    return translator.batch_translate(
        texts=request.texts,
        target_language=request.target_language,
        source_language=request.source_language
    )