import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential

def check_safety_of_text(text: str):
    endpoint = os.environ.get("CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("CONTENT_SAFETY_ENDPOINT and CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    request = AnalyzeTextOptions(
        text=text,
        categories=[TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE]
    )

    response = client.analyze_text(request)

    safety_analysis = {
        "hate": response.hate_result.severity if response.hate_result else 0,
        "self_harm": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual": response.sexual_result.severity if response.sexual_result else 0,
        "violence": response.violence_result.severity if response.violence_result else 0,
    }
    return safety_analysis
