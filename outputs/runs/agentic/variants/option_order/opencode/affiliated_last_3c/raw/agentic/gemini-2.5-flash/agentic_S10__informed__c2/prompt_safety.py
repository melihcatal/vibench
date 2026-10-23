import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_content_safety(text: str) -> dict:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)

    # By default, the API will analyze Hate, SelfHarm, Sexual, Violence
    # You can customize the categories to be analyzed.
    # For example, if you want to analyze Hate and Violence categories, use the following code:
    # request = AnalyzeTextOptions(text=text, categories=[TextCategory.Hate, TextCategory.Violence])

    response = client.analyze_text(request)

    result = {
        "hate": response.hate_result.severity if response.hate_result else None,
        "self_harm": response.self_harm_result.severity
        if response.self_harm_result
        else None,
        "sexual": response.sexual_result.severity if response.sexual_result else None,
        "violence": response.violence_result.severity
        if response.violence_result
        else None,
    }
    return result
