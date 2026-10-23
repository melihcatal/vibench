import os
import requests
from typing import List, Dict, Any


class AzureContentSafetyClient:
    def __init__(self):
        self.endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
        if not self.endpoint or not self.key:
            raise ValueError(
                "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
            )
        self.api_version = "2023-10-15-preview"
        self.headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json",
        }

    def moderate_text(self, text: str) -> Dict[str, Any]:
        url = f"{self.endpoint}/content safetyscan/text:analyze?api-version={self.api_version}"
        payload = {"text": text}
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def moderate_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        results = []
        for text in texts:
            results.append(self.moderate_text(text))
        return results

    def redact_unsafe_content(self, text: str) -> Dict[str, Any]:
        url = f"{self.endpoint}/content safetyscan/text:analyze?api-version={self.api_version}"
        payload = {
            "text": text,
            "outputType": "FourSeverityLevels",
        }  # This will include information for redaction
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
