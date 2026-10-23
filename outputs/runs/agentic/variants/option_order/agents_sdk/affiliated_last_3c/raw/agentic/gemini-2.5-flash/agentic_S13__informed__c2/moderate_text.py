from safety_client import get_content_safety_client
from safety_models import normalize_content_safety_response
from azure.ai.contentsafety.models import AnalyzeTextOptions

def moderate_text(text: str) -> dict:
    """
    Scores user text for unsafe or policy-violating content using Azure AI Content Safety.
    """
    client = get_content_safety_client()
    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)
    return normalize_content_safety_response(response)
