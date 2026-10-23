import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential


def moderate_vendor_notes(text: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY not set."
        )

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

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

    # Example of parsing the response, adjust as needed based on desired output
    safety_analysis = {
        "hate_result": response.hate_result.severity if response.hate_result else None,
        "self_harm_result": response.self_harm_result.severity
        if response.self_harm_result
        else None,
        "sexual_result": response.sexual_result.severity
        if response.sexual_result
        else None,
        "violence_result": response.violence_result.severity
        if response.violence_result
        else None,
    }
    return safety_analysis
