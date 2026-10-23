from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions
import os


def moderate_text(text: str) -> bool:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    return all(result.severity <= 2 for result in response.categories_analysis)


def profile_moderation(profile_text: str) -> bool:
    return moderate_text(profile_text)


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        profile_text = sys.argv[1]
        is_safe = profile_moderation(profile_text)
        print(f"Profile text is safe: {is_safe}")
