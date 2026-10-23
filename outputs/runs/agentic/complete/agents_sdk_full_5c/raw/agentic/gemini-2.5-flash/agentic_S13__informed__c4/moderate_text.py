import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_text(text: str):
    """Scores user text for unsafe or policy-violating content using Azure AI Content Safety."""
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
        output_type="FourSeverityLevels",
    )

    try:
        response = client.analyze_text(request)
        return {
            "text": text,
            "hate": response.categories_analysis[0].severity,
            "self_harm": response.categories_analysis[1].severity,
            "sexual": response.categories_analysis[2].severity,
            "violence": response.categories_analysis[3].severity,
        }
    except Exception as e:
        print(f"Error moderating text with Azure AI Content Safety: {e}")
        return None
