import os
from typing import Optional, Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions


class SafetyClient:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

        if not self.endpoint or not self.key:
            raise ValueError(
                "Azure Content Safety credentials not configured. "
                "Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables."
            )

        self.client = ContentSafetyClient(self.endpoint, AzureKeyCredential(self.key))

    def analyze_text(
        self, text: str, categories: Optional[list] = None
    ) -> Dict[str, Any]:
        request = AnalyzeTextOptions(text=text)
        response = self.client.analyze_text(request)

        result = {
            "text": text,
            "categories": [],
            "has_violations": False,
            "provider": "azure_content_safety",
        }

        for category_result in response.categories_analysis:
            category_info = {
                "category": category_result.category.value,
                "severity": category_result.severity,
                "severity_level": category_result.severity,
            }
            result["categories"].append(category_info)

            if category_result.severity > 0:
                result["has_violations"] = True

        return result

    def get_client(self):
        return self.client

    @staticmethod
    def validate_config() -> bool:
        endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        return bool(endpoint and key)
