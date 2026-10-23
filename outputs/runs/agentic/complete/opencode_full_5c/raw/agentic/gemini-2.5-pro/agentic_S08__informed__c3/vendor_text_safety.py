import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_vendor_text_safety(text_to_moderate: str) -> dict:
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_to_moderate,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed. Reason: {e.reason}")
        return {}

    return {
        "hate_result": response.hate_result.severity if response.hate_result else 0,
        "self_harm_result": response.self_harm_result.severity
        if response.self_harm_result
        else 0,
        "sexual_result": response.sexual_result.severity
        if response.sexual_result
        else 0,
        "violence_result": response.violence_result.severity
        if response.violence_result
        else 0,
    }
