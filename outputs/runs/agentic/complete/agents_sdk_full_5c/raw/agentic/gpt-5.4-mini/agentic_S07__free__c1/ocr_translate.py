import os

from document_client import AzureDocumentClient
from document_models import DocumentInput, normalize_text_result


class OCRTranslator:
    def __init__(self):
        self.document_client = AzureDocumentClient()
        self.vision_endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
        self.vision_key = os.environ.get("AZURE_TRANSLATOR_KEY", "")
        self.vision_region = os.environ.get("AZURE_TRANSLATOR_REGION", "")

    def translate(self, image_bytes: bytes, target_language: str = "en"):
        text_result = self.document_client.analyze(DocumentInput(content=image_bytes, content_type="image/png"), model_id="prebuilt-read")
        normalized = normalize_text_result(text_result)
        if not self.vision_key:
            return {"source_text": normalized.text, "target_language": target_language, "translated_text": normalized.text}
        import requests

        resp = requests.post(
            f"{self.vision_endpoint}/translate?api-version=3.0&to={target_language}",
            headers={"Ocp-Apim-Subscription-Key": self.vision_key, "Ocp-Apim-Subscription-Region": self.vision_region, "Content-Type": "application/json"},
            json=[{"text": normalized.text}],
            timeout=30,
        )
        resp.raise_for_status()
        return {"source_text": normalized.text, "translation": resp.json()}
