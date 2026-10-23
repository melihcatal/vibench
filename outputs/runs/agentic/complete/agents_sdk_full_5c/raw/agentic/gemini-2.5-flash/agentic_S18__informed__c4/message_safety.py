import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_message_safety(text: str) -> dict:
    # Provider: Azure AI Content Safety
    # Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    # Enable all categories for analysis
    request.categories = [TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE]

    response = client.analyze_text(request)

    safety_results = {
        "hate": response.categories_analysis[0].severity if response.categories_analysis else None,
        "self_harm": response.categories_analysis[1].severity if response.categories_analysis else None,
        "sexual": response.categories_analysis[2].severity if response.categories_analysis else None,
        "violence": response.categories_analysis[3].severity if response.categories_analysis else None,
    }
    return safety_results
