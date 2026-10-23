import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from typing import List
from safety_models import ModerationResult, CategoryDetection, TextContent


class ContentSafetyClientWrapper:
    def __init__(self):
        self.endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
        if not self.endpoint or not self.key:
            raise ValueError(
                "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
            )
        self.client = ContentSafetyClient(self.endpoint, AzureKeyCredential(self.key))

    def moderate_text(self, text_content: TextContent) -> ModerationResult:
        request = AnalyzeTextOptions(text=text_content.text)
        response = self.client.analyze_text(request)

        categories_detection = []
        is_unsafe = False

        for category in response.categories_analysis:
            categories_detection.append(
                CategoryDetection(
                    category=category.category, severity=category.severity
                )
            )
            if category.severity > 0:
                is_unsafe = True

        return ModerationResult(
            text=text_content.text,
            categories_detection=categories_detection,
            is_unsafe=is_unsafe,
        )

    def moderate_batch(self, texts: List[TextContent]) -> List[ModerationResult]:
        results = []
        for text_content in texts:
            results.append(self.moderate_text(text_content))
        return results
