import os
from typing import Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


class AzureContentModerator:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        self.client = ContentSafetyClient(self.endpoint, AzureKeyCredential(self.key))

    def moderate_text(self, text: str) -> Dict[str, Any]:
        request = AnalyzeTextOptions(
            text=text,
            categories=[
                TextCategory.HATE,
                TextCategory.SELF_HARM,
                TextCategory.SEXUAL,
                TextCategory.VIOLENCE,
            ],
        )
        response = self.client.analyze_text(request)
        return {
            "blocked": any(
                result.severity > 2 for result in response.categories_analysis
            ),
            "categories": {
                result.category.value: result.severity
                for result in response.categories_analysis
            },
        }


def profile_moderation(text: str) -> Dict[str, Any]:
    moderator = AzureContentModerator()
    return moderator.moderate_text(text)
