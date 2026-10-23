import os
from typing import Dict, Any
from security_models import TranslationResult
from google.cloud import translate_v2 as translate


class ComplianceNoteTranslator:
    def __init__(self):
        self.client = translate.Client.from_service_account_json(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )

    def translate_compliance_note(
        self, text: str, target_language: str = "es"
    ) -> TranslationResult:
        try:
            result = self.client.translate(text, target_language=target_language)

            return TranslationResult(
                translated_text=result["translatedText"],
                source_language=result["detectedSourceLanguage"],
                target_language=target_language,
            )
        except Exception as e:
            raise Exception(f"Google Cloud Translation failed: {e}")
