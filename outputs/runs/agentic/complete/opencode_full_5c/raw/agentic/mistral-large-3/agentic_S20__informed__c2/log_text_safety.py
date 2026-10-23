import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError


class LogTextSafetyChecker:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        self.client = ContentSafetyClient(self.endpoint, AzureKeyCredential(self.key))

    def check_text_safety(self, text: str) -> Dict[str, Any]:
        try:
            request = {
                "text": text,
                "categories": ["Hate", "Sexual", "SelfHarm", "Violence"],
            }
            response = self.client.analyze_text(request)
            return {
                "is_safe": all(
                    result.severity == 0 for result in response.categories_analysis
                ),
                "results": {
                    result.category: result.severity
                    for result in response.categories_analysis
                },
            }
        except AzureError as e:
            raise Exception(f"Azure Content Safety API error: {e}")


if __name__ == "__main__":
    checker = LogTextSafetyChecker()
    result = checker.check_text_safety(
        "This is a test log message with no unsafe content."
    )
    print(result)
