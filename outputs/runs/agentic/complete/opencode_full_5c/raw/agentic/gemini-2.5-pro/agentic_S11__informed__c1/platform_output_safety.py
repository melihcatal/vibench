import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from model_models import SafetyResult


def check_content_safety(text_to_analyze: str) -> SafetyResult:
    """
    Checks text for harmful content using Azure AI Content Safety.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_to_analyze)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed. {e}")
        return SafetyResult(is_safe=False, raw_result=e)

    is_safe = all(
        category.severity == 0
        for category in [
            response.hate_result,
            response.self_harm_result,
            response.sexual_result,
            response.violence_result,
        ]
    )

    return SafetyResult(is_safe=is_safe, raw_result=response)
