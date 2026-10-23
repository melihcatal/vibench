import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from typing import Dict

def check_text_safety(record: Dict[str, any]) -> dict:
    """
    Checks user-generated text fields in a record for harmful content
    using Azure AI Content Safety.

    Args:
        record: A dictionary representing the document record,
                containing text fields like 'content' or 'author'.

    Returns:
        A dictionary with the analysis results for each category.
    """
    try:
        endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
        key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    except KeyError:
        raise EnvironmentError("Missing environment variables: AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
    text_to_analyze = record.get("content", "")
    if not text_to_analyze:
        return {"status": "No text provided."}

    request = AnalyzeTextOptions(text=text_to_analyze)

    try:
        response = client.analyze_text(request)
    except Exception as e:
        return {"status": f"Error analyzing text with Azure Content Safety: {e}"}

    results = {
        "hate": response.hate_result.severity,
        "self_harm": response.self_harm_result.severity,
        "sexual": response.sexual_result.severity,
        "violence": response.violence_result.severity,
    }
    
    return results
