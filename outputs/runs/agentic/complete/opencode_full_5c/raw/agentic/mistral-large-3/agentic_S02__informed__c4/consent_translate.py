import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate


class ConsentTranslator:
    def __init__(self):
        self.client = translate.Client.from_service_account_json(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )

    def translate_consent(self, text: str, target_language: str) -> Dict[str, Any]:
        result = self.client.translate(text, target_language=target_language)
        return {
            "original_text": text,
            "translated_text": result["translatedText"],
            "detected_language": result["detectedSourceLanguage"],
        }


if __name__ == "__main__":
    translator = ConsentTranslator()
    sample_text = "I agree to the terms and conditions."
    result = translator.translate_consent(sample_text, "es")
    print("Translation Result:", result)
