"""
[LATER-STEP] visual_safety_text.py - Check generated visual labels for unsafe text
"""
import os
from typing import List
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_text_safety(text_list: List[str]) -> dict:
    """
    Analyzes a list of text strings for harmful content using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials are not set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
    full_text = " ".join(text_list)
    if not full_text.strip():
        return {"safe": True, "results": {}}

    request = AnalyzeTextOptions(text=full_text)
    
    safety_results = {}

    try:
        response = client.analyze_text(request)
        safety_results['hate'] = response.hate_result.severity if response.hate_result else 0
        safety_results['self_harm'] = response.self_harm_result.severity if response.self_harm_result else 0
        safety_results['sexual'] = response.sexual_result.severity if response.sexual_result else 0
        safety_results['violence'] = response.violence_result.severity if response.violence_result else 0
        
        is_safe = all(severity == 0 for severity in safety_results.values())
        
        return {"safe": is_safe, "results": safety_results}

    except HttpResponseError as e:
        print(f"Error analyzing text with Azure Content Safety: {e}")
        return {"safe": False, "error": str(e)}
