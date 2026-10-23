from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions
import os


class AzureContentSafetyChecker:
    def __init__(self):
        self.client = ContentSafetyClient(
            endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
            credential=AzureKeyCredential(os.getenv("AZURE_CONTENT_SAFETY_KEY")),
        )

    def check_secret_label_safety(self, text: str) -> dict:
        request = AnalyzeTextOptions(text=text)
        response = self.client.analyze_text(request)

        return {
            "hate_result": response.hate_result,
            "self_harm_result": response.self_harm_result,
            "sexual_result": response.sexual_result,
            "violence_result": response.violence_result,
            "is_safe": all(
                result.severity == 0
                for result in [
                    response.hate_result,
                    response.self_harm_result,
                    response.sexual_result,
                    response.violence_result,
                ]
            ),
        }
