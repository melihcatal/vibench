import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from typing import List


def check_content_safety(text: str) -> dict:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    response = client.analyze_text(request)

    result = {
        "hate_score": response.hate_result.severity if response.hate_result else 0,
        "self_harm_score": response.self_harm_result.severity
        if response.self_harm_result
        else 0,
        "sexual_score": response.sexual_result.severity
        if response.sexual_result
        else 0,
        "violence_score": response.violence_result.severity
        if response.violence_result
        else 0,
    }
    return result
