import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from typing import Dict, Any


def check_text_safety(text_content: str) -> Dict[str, Any]:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_content,
        categories=[
            TextCategory.HATE,
            TextCategory.VIOLENCE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
        ],
        blocklist_names=[],
    )

    response = client.analyze_text(request)

    result = {}
    if response.hate_result:
        result["hate"] = {"severity": response.hate_result.severity}
    if response.violence_result:
        result["violence"] = {"severity": response.violence_result.severity}
    if response.self_harm_result:
        result["self_harm"] = {"severity": response.self_harm_result.severity}
    if response.sexual_result:
        result["sexual"] = {"severity": response.sexual_result.severity}

    return result
