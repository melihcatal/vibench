import os
from typing import Optional
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from .safety_models import (
    SafetyRequest,
    SafetyResponse,
    BatchSafetyRequest,
    BatchSafetyResponse,
)


class SafetyClient:
    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        self.endpoint = endpoint or os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = key or os.getenv("AZURE_CONTENT_SAFETY_KEY")

        if not self.endpoint or not self.key:
            raise ValueError("Azure Content Safety credentials not configured")

        self.client = ContentSafetyClient(self.endpoint, AzureKeyCredential(self.key))

    def get_client(self) -> ContentSafetyClient:
        return self.client

    def create_request(self, text: str, categories: list = None) -> SafetyRequest:
        if categories is None:
            categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

        return SafetyRequest(text=text, categories=categories)

    def parse_response(self, azure_response) -> SafetyResponse:
        categories = {}
        for category in azure_response.categories_analysis:
            categories[category.category] = {
                "severity": category.severity,
                "score": category.severity_score,
            }

        return SafetyResponse(
            text=azure_response.text if hasattr(azure_response, "text") else "",
            categories=categories,
        )

    def create_batch_request(self, texts: list) -> BatchSafetyRequest:
        return BatchSafetyRequest(texts=texts)

    def parse_batch_response(self, responses: list) -> BatchSafetyResponse:
        results = []
        for response in responses:
            results.append(self.parse_response(response))
        return BatchSafetyResponse(results=results)
