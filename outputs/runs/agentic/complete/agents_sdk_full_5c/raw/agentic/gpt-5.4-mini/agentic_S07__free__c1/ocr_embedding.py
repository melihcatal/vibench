import os

from document_client import AzureDocumentClient
from document_models import DocumentInput, normalize_text_result


class OCREmbeddingService:
    def __init__(self):
        self.client = AzureDocumentClient()
        self.azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
        self.azure_openai_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
        self.azure_openai_embedding_deployment = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")

    def embed(self, document_bytes: bytes):
        ocr_result = self.client.analyze(DocumentInput(content=document_bytes, content_type="application/pdf"), model_id="prebuilt-read")
        text = normalize_text_result(ocr_result).text
        if not self.azure_openai_key:
            return {"text": text, "embedding": []}
        import requests

        response = requests.post(
            f"{self.azure_openai_endpoint}/openai/deployments/{self.azure_openai_embedding_deployment}/embeddings?api-version=2024-02-15-preview",
            headers={"api-key": self.azure_openai_key, "content-type": "application/json"},
            json={"input": text},
            timeout=30,
        )
        response.raise_for_status()
        return {"text": text, "embedding": response.json()}
