import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_corpus_safety(text: str) -> dict:
    """Checks corpus text for safety using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY environment variables not set."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE_SPEECH,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
            TextCategory.SELF_HARM,
        ],
    )

    try:
        response = client.analyze_text(request)
        safety_results = {"categories_analysis": []}
        for category_result in response.categories_analysis:
            safety_results["categories_analysis"].append(
                {
                    "category": category_result.category.value,
                    "severity": category_result.severity,
                }
            )
        return safety_results
    except Exception as e:
        print(f"Error checking corpus safety: {e}")
        return {}
