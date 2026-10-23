# vendor_text_safety.py
from document_client import get_azure_content_safety_client
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_vendor_notes(text: str) -> dict:
    """
    Moderates vendor notes or memo fields using Azure Content Safety.
    
    Args:
        text: The text to be analyzed.
        
    Returns:
        A dictionary with the analysis results.
    """
    if not text.strip():
        return {"safe": True, "categories": {}}

    client = get_azure_content_safety_client()
    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed. Error code: {e.error.code}, Error message: {e.error.message}")
        raise

    results = {"safe": True, "categories": {}}
    if response.hate_result:
        results["categories"]["hate"] = response.hate_result.severity
        if response.hate_result.severity > 0: results["safe"] = False
    if response.self_harm_result:
        results["categories"]["self_harm"] = response.self_harm_result.severity
        if response.self_harm_result.severity > 0: results["safe"] = False
    if response.sexual_result:
        results["categories"]["sexual"] = response.sexual_result.severity
        if response.sexual_result.severity > 0: results["safe"] = False
    if response.violence_result:
        results["categories"]["violence"] = response.violence_result.severity
        if response.violence_result.severity > 0: results["safe"] = False
        
    return results
