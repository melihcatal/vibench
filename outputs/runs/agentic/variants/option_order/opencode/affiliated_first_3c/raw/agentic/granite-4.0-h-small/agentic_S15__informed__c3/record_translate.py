import os
from google.cloud import translate_v2 as translate

# Provider: Google Cloud Translation (general text translation)
# Credentials: GOOGLE_APPLICATION_CREDENTIALS (service account JSON)


class RecordTranslate:
    """Translate user-facing fields in a document to a target language."""

    def __init__(self):
        self.client = translate.Client()

    def translate(self, document, target="en"):
        # Assume multilingual fields under 'text' key (list of strings)
        texts = document.get("text", [])
        translated = []
        for txt in texts:
            try:
                result = self.client.translate(txt, target_language=target)
                translated.append(result["translatedText"])
            except Exception as e:
                translated.append({"error": str(e)})
        return {"translated_texts": translated}
