import os
from typing import List
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalyzeRequest, AnalyzeTextOptions


def unsafe_copy_check(texts: List[str]) -> Dict[str, List[str]]:
    """
    Checks localized copy for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    results = {}

    for i, text in enumerate(texts):
        request = AnalyzeTextOptions(text=text)
        response = client.analyze_text(request)
        issues = []
        if response.hate_result.severity > 0:
            issues.append(
                f"Hate content detected (severity: {response.hate_result.severity})"
            )
        if response.self_harm_result.severity > 0:
            issues.append(
                f"Self-harm content detected (severity: {response.self_harm_result.severity})"
            )
        if response.sexual_result.severity > 0:
            issues.append(
                f"Sexual content detected (severity: {response.sexual_result.severity})"
            )
        if response.violence_result.severity > 0:
            issues.append(
                f"Violence content detected (severity: {response.violence_result.severity})"
            )
        results[f"text_{i}"] = issues if issues else ["No issues detected"]

    return results
