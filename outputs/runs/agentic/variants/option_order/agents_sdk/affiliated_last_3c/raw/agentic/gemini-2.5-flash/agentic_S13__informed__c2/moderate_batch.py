from typing import List
from safety_client import get_content_safety_client
from safety_models import normalize_content_safety_response
from azure.ai.contentsafety.models import AnalyzeTextOptions

def moderate_batch(texts: List[str]) -> List[dict]:
    """
    Moderates a batch of user messages and returns per-message decisions using Azure AI Content Safety.
    """
    client = get_content_safety_client()
    results = []
    for text in texts:
        request = AnalyzeTextOptions(text=text)
        response = client.analyze_text(request)
        results.append(normalize_content_safety_response(response))
    return results
