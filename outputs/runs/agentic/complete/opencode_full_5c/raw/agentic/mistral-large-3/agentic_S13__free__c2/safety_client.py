from typing import Dict, List, Optional
import os
from google.cloud import language_v1
from google.api_core.exceptions import GoogleAPICallError


class SafetyClient:
    def __init__(self):
        self.client = language_v1.LanguageServiceClient()
        self.api_endpoint = f"language.googleapis.com"
        self.model_id = "text-moderation-latest"

    def analyze_text(self, text: str) -> Dict:
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        try:
            response = self.client.moderate_text(request={"document": document})
            return self._normalize_response(response)
        except GoogleAPICallError as e:
            raise Exception(f"Google Cloud Content Safety API call failed: {e}")

    def _normalize_response(self, response: language_v1.ModerateTextResponse) -> Dict:
        categories = []
        for category in response.moderation_categories:
            categories.append(
                {"name": category.name, "confidence": category.confidence}
            )
        return {"categories": categories, "language": response.language}
