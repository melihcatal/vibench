import os
from google.cloud import translate_v2 as translate


class ComplianceNoteTranslator:
    def __init__(self):
        # Google Cloud Translation client requires GOOGLE_APPLICATION_CREDENTIALS
        # or other forms of authentication to be set up in the environment.
        # Provider-identifying signal: google.cloud.translate_v2
        self.client = translate.Client()

    def translate_text(self, text: str, target_language: str = "en") -> dict:
        if not text:
            return {"translated_text": "", "detected_source_language": ""}

        try:
            # The translate method returns a dictionary with the translated text and detected source language.
            result = self.client.translate(text, target_language=target_language)

            return {
                "translated_text": result["translatedText"],
                "detected_source_language": result["detectedSourceLanguage"],
            }
        except Exception as e:
            return {"error": f"Error translating text: {e}"}
