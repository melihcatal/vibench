import os
import json
from google.cloud import translate_v2 as translate

# Later-step scored file – translate extracted OCR text
# Uses Google Cloud Translation API (concrete provider)


class OcrTranslate:
    def __init__(self):
        # Expect GOOGLE_APPLICATION_CREDENTIALS env var with path to JSON key
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path or not os.path.isfile(credentials_path):
            raise RuntimeError(
                "Set GOOGLE_APPLICATION_CREDENTIALS env var to a valid JSON key file"
            )
        translate.Client()  # Initializes client using credentials_path

    def translate(self, source_text: str, target_lang: str = "en") -> str:
        client = translate.Client()
        result = client.translate(source_text, target_language=target_lang)
        # result["translatedText"] contains the translation
        return result["translatedText"]


if __name__ == "__main__":
    translator = OcrTranslate()
    extracted = "Voici un exemple de document numérisé en français."
    translated = translator.translate(extracted, target_lang="en")
    print("Translation:", translated)
