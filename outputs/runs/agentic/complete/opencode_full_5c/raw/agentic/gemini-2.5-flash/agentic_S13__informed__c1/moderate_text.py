import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY")


def moderate_text(text: str):
    client = ContentSafetyClient(
        endpoint=AZURE_CONTENT_SAFETY_ENDPOINT,
        credential=AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY),
    )
    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE_SPEECH,
            TextCategory.VIOLENCE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
        ],
    )
    response = client.analyze_text(request)
    return {
        category.category.value: category.severity for category in response.categories
    }
