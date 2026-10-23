import os
from azure.ai.contentsafety import ContentSafetyClient


class SafetyClient:
    def __init__(self):
        self.client = ContentSafetyClient(
            endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
            credential=os.getenv("AZURE_CONTENT_SAFETY_KEY"),
        )

    def analyze_text(self, text):
        from azure.ai.contentsafety.models import AnalyzeTextOptions

        options = AnalyzeTextOptions(text=text)
        return self.client.analyze_text(options)
