import os
from typing import List, Dict
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalyzeRequest, AnalyzeTextOptions

def moderate_transcript(text_segments: List[str]) -> List[Dict]:
    """
    Moderate transcript segments using Azure AI Content Safety.
    Returns a list of moderation results for each segment.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    results = []
    for segment in text_segments:
        request = AnalyzeTextOptions(text=segment)
        response = client.analyze_text(request)
        results.append({
            "hate_result": response.hate_result,
            "self_harm_result": response.self_harm_result,
            "sexual_result": response.sexual_result,
            "violence_result": response.violence_result
        })
    return results