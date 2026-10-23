from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from typing import Dict, Any, Optional
import os

class VendorTextSafety:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        self.client = self._initialize_client()

    def _initialize_client(self) -> Optional[ContentSafetyClient]:
        if not self.endpoint or not self.key:
            return None
        try:
            return ContentSafetyClient(self.endpoint, AzureKeyCredential(self.key))
        except Exception:
            return None

    def moderate_text(self, text: str) -> Dict[str, Any]:
        if not self.client or not text:
            return {"safe": False, "reasons": ["Client not initialized or empty text"]}

        try:
            request = AnalyzeTextOptions(text=text, categories=[
                TextCategory.HATE,
                TextCategory.SELF_HARM,
                TextCategory.SEXUAL,
                TextCategory.VIOLENCE
            ])
            response = self.client.analyze_text(request)

            results = {
                "safe": True,
                "reasons": [],
                "details": {}
            }

            for category in response.categories_analysis:
                if category.severity > 2:
                    results["safe"] = False
                    results["reasons"].append(category.category.value)
                results["details"][category.category.value] = category.severity

            return results
        except Exception as e:
            return {"safe": False, "reasons": [str(e)]}

    def check_vendor_notes(self, normalized_data: Dict[str, Any]) -> Dict[str, Any]:
        vendor_notes = normalized_data.get("metadata", {}).get("original_fields", {}).get("vendor_notes", "")
        return self.moderate_text(vendor_notes)