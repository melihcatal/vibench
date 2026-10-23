from google.cloud import translate_v2 as translate
import os


# Provider: Google Cloud Translation API
class ComplianceNoteTranslator:
    def __init__(self):
        self.client = translate.Client()
        self.target_languages = {
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "ja": "Japanese",
            "zh": "Chinese (Simplified)",
        }

    def translate_compliance_note(self, note: str, target_language: str) -> dict:
        if target_language not in self.target_languages:
            raise ValueError(f"Unsupported target language: {target_language}")

        result = self.client.translate(note, target_language=target_language)

        return {
            "translated_text": result["translatedText"],
            "source_language": result["detectedSourceLanguage"],
            "target_language": target_language,
            "target_language_name": self.target_languages[target_language],
            "provider": "google_cloud_translation",
        }


def translate_compliance_note(note: str, target_language: str) -> dict:
    translator = ComplianceNoteTranslator()
    return translator.translate_compliance_note(note, target_language)
