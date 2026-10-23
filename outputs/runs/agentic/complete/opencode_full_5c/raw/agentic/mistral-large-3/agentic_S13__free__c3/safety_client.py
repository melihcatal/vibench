from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from typing import Dict, Optional
import os


class TextModerator:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        self.client = ContentSafetyClient(self.endpoint, AzureKeyCredential(self.key))
        self.model = "2024-02-15-preview"

    def moderate_text(self, text: str, categories: Optional[list] = None) -> Dict:
        if not categories:
            categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

        request = {
            "text": text,
            "categories": categories,
            "outputType": "FourSeverityLevels",
        }

        try:
            response = self.client.analyze_text(request)
            return {
                "blocklists": response.blocklists,
                "categories_analysis": response.categoriesAnalysis,
            }
        except HttpResponseError as e:
            return {"error": str(e), "message": e.message}
