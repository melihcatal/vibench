from typing import Dict, Any
import os
import requests


class VendorTextSafety:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    def moderate_text(self, text: str) -> Dict[str, Any]:
        if not text:
            return {"is_safe": True, "categories": []}

        url = f"{self.endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json",
        }
        body = {"text": text, "categories": ["Hate", "Sexual", "SelfHarm", "Violence"]}

        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        result = response.json()

        is_safe = all(
            blocklist_result["severity"] == 0
            for blocklist_result in result.get("blocklistsMatchResults", [])
        ) and all(
            category["severity"] == 0
            for category in result.get("categoriesAnalysis", [])
        )

        return {"is_safe": is_safe, "categories": result.get("categoriesAnalysis", [])}
