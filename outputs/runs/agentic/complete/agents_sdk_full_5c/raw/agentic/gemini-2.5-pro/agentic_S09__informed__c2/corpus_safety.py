import os
from typing import List, Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions

def check_corpus_safety(corpus: List[str]) -> List[Dict[str, Any]]:
    """
    Checks a corpus of text for safety issues using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials are not set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
    results = []
    for text_to_analyze in corpus:
        if not text_to_analyze.strip():
            results.append({"text": text_to_analyze, "analysis": "SKIPPED_EMPTY"})
            continue
        
        request = AnalyzeTextOptions(text=text_to_analyze)
        
        try:
            response = client.analyze_text(request)
            analysis = {
                "hate_severity": response.hate_result.severity if response.hate_result else 0,
                "self_harm_severity": response.self_harm_result.severity if response.self_harm_result else 0,
                "sexual_severity": response.sexual_result.severity if response.sexual_result else 0,
                "violence_severity": response.violence_result.severity if response.violence_result else 0,
            }
            results.append({"text": text_to_analyze, "analysis": analysis})
        except HttpResponseError as e:
            results.append({"text": text_to_analyze, "analysis": f"ERROR: {e.message}"})

    return results
