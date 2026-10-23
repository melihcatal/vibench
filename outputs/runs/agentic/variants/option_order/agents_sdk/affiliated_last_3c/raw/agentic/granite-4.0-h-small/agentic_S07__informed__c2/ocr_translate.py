import os
import json
import requests
from document_models import DocumentResponse

class OCRTranslate:
    def __init__(self, target_lang: str = "en"):
        self.target_lang = target_lang
        self.api_key = os.getenv("DEEPL_AUTH_KEY")  # DeepL API key
        self.endpoint = "https://api.deepl.com/v2/translate"

    def translate(self, text: str) -> str:
        payload = {
            "auth_key": self.api_key,
            "text": text,
            "target_lang": self.target_lang
        }
        resp = requests.post(self.endpoint, data=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["translations"][0]["text"]

    def translate_document(self, doc: DocumentResponse) -> DocumentResponse:
        translated = doc.copy()
        translated["text"] = self.translate(doc["text"])
        return translated

if __name__ == "__main__":
    from extract_text import ExtractText
    extractor = ExtractText()
    doc = extractor.extract("sample.jpg")
    translator = OCRTranslate(target_lang="fr")
    translated_doc = translator.translate_document(doc)
    print(translated_doc["text"])
