import os
from dotenv import load_dotenv
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

load_dotenv()


def check_corpus_safety(text_to_analyze: str) -> dict:
    """
    Check corpus text for safety issues before embedding using Azure Content Safety.
    """
    endpoint = os.getenv("CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("CONTENT_SAFETY_ENDPOINT and CONTENT_SAFETY_KEY must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_to_analyze)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"Analyze text failed: {e.message}"}

    return {
        "hate_severity": response.hate_result.severity if response.hate_result else 0,
        "self_harm_severity": response.self_harm_result.severity
        if response.self_harm_result
        else 0,
        "sexual_severity": response.sexual_result.severity
        if response.sexual_result
        else 0,
        "violence_severity": response.violence_result.severity
        if response.violence_result
        else 0,
    }
