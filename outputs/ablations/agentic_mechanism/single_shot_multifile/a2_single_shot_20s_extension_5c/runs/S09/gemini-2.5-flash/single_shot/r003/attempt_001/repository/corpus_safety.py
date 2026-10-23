import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_corpus_safety(text: str) -> dict:
    """Checks a given text for safety using Azure Content Safety.
    Returns a dictionary of moderation results for different categories."""
    
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be set as environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text,
        categories=[TextCategory.HATE, TextCategory.VIOLENCE, TextCategory.SELF_HARM, TextCategory.SEXUAL],
        blocklist_names=["MyBlocklist"] # Optional: if you have a custom blocklist
    )

    response = client.analyze_text(request)

    results = {}
    if response.hate_result:
        results["hate"] = {"category": response.hate_result.category.value, "severity": response.hate_result.severity}
    if response.violence_result:
        results["violence"] = {"category": response.violence_result.category.value, "severity": response.violence_result.severity}
    if response.self_harm_result:
        results["self_harm"] = {"category": response.self_harm_result.category.value, "severity": response.self_harm_result.severity}
    if response.sexual_result:
        results["sexual"] = {"category": response.sexual_result.category.value, "severity": response.sexual_result.severity}
    
    return results