import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_safety(text_to_analyze: str) -> dict:
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_to_analyze,
        categories=[
            TextCategory.HATRED,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"Analyze text failed. {e.message}"}

    return {
        "hateResult": response.hate_result.severity if response.hate_result else None,
        "selfHarmResult": response.self_harm_result.severity
        if response.self_harm_result
        else None,
        "sexualResult": response.sexual_result.severity
        if response.sexual_result
        else None,
        "violenceResult": response.violence_result.severity
        if response.violence_result
        else None,
    }
