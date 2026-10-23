import os

from document_client import AzureDocumentClient
from document_models import DocumentInput, normalize_text_result


class DocumentFieldExtractor:
    def __init__(self):
        self.client = AzureDocumentClient()
        self.azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
        self.azure_openai_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
        self.azure_openai_deployment = os.environ.get("AZURE_OPENAI_FIELD_EXTRACTION_DEPLOYMENT", "gpt-4o-mini")

    def extract(self, document_bytes: bytes):
        ocr_result = self.client.analyze(DocumentInput(content=document_bytes, content_type="application/pdf"), model_id="prebuilt-read")
        normalized = normalize_text_result(ocr_result)
        if not self.azure_openai_key:
            return {"text": normalized.text, "fields": {}}
        import requests

        payload = {
            "messages": [
                {"role": "system", "content": "Extract structured fields from OCR text and return JSON."},
                {"role": "user", "content": normalized.text},
            ],
            "temperature": 0,
        }
        response = requests.post(
            f"{self.azure_openai_endpoint}/openai/deployments/{self.azure_openai_deployment}/chat/completions?api-version=2024-02-15-preview",
            headers={"api-key": self.azure_openai_key, "content-type": "application/json"},
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return {"text": normalized.text, "fields": response.json()}
