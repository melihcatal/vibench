import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential


def check_live_caption_safety(text: str):  # Using Azure AI Content Safety
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    try:
        request = AnalyzeTextOptions(text=text)
        response = client.analyze_text(request)

        safety_results = {
            "hate": response.hate_result.severity,
            "self_harm": response.self_harm_result.severity,
            "sexual": response.sexual_result.severity,
            "violence": response.violence_result.severity,
        }
        return safety_results
    except Exception as e:
        print(f"Content Safety error: {e}")
        return None
