from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions
import os


class SecretLabelSafetyChecker:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        if not self.endpoint or not self.key:
            raise ValueError("Azure Content Safety endpoint or key not set")
        self.client = ContentSafetyClient(self.endpoint, AzureKeyCredential(self.key))

    def check_secret_label_safety(self, text: str) -> Dict[str, Any]:
        request = AnalyzeTextOptions(text=text)
        response = self.client.analyze_text(request)
        return {
            "hate_result": response.hate_result,
            "self_harm_result": response.self_harm_result,
            "sexual_result": response.sexual_result,
            "violence_result": response.violence_result,
            "is_safe": all(
                category.severity == 0
                for category in [
                    response.hate_result,
                    response.self_harm_result,
                    response.sexual_result,
                    response.violence_result,
                ]
            ),
        }
