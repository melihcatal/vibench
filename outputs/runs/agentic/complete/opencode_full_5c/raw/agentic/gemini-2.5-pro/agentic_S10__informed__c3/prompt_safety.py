import os
from typing import List
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from model_models import SafetyResult


def check_prompt_safety(prompt: str) -> List[SafetyResult]:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety credentials not found in environment variables."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=prompt)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed. Error message: {e.message}")
        return []

    results = []
    if response.hate_result:
        results.append(
            SafetyResult(
                category=TextCategory.HATE, severity=response.hate_result.severity
            )
        )
    if response.self_harm_result:
        results.append(
            SafetyResult(
                category=TextCategory.SELF_HARM,
                severity=response.self_harm_result.severity,
            )
        )
    if response.sexual_result:
        results.append(
            SafetyResult(
                category=TextCategory.SEXUAL, severity=response.sexual_result.severity
            )
        )
    if response.violence_result:
        results.append(
            SafetyResult(
                category=TextCategory.VIOLENCE,
                severity=response.violence_result.severity,
            )
        )

    return results
