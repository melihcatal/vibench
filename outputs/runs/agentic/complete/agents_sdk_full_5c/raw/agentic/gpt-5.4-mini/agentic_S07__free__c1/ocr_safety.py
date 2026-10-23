import os

from document_client import AzureDocumentClient
from document_models import DocumentInput, normalize_text_result


class OCRSafetyChecker:
    def __init__(self):
        self.client = AzureDocumentClient()
        self.azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
        self.azure_openai_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
        self.azure_openai_deployment = os.environ.get("AZURE_OPENAI_CONTENT_SAFETY_DEPLOYMENT", "text-moderation-preview")

    def check(self, image_bytes: bytes):
        result = self.client.analyze(DocumentInput(content=image_bytes, content_type="image/png"), model_id="prebuilt-read")
        text = normalize_text_result(result).text
        if not self.azure_openai_key:
            return {"safe": True, "text": text}
        import requests

        response = requests.post(
            f"{self.azure_openai_endpoint}/openai/deployments/{self.azure_openai_deployment}/moderations?api-version=2024-02-15-preview",
            headers={"api-key": self.azure_openai_key, "content-type": "application/json"},
            json={"input": text},
            timeout=30,
        )
        response.raise_for_status()
        return {"safe": True, "moderation": response.json(), "text": text}
