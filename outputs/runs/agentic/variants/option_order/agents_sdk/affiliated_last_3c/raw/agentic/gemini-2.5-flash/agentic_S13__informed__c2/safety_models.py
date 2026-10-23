from typing import List, Dict, Any

def normalize_content_safety_response(response: Any) -> Dict[str, Any]:
    """
    Normalizes the response from the Azure AI Content Safety service.
    """
    categories = {}
    if response.hate_result:
        categories["Hate"] = {"severity": response.hate_result.severity, "detected": response.hate_result.severity > 0}
    if response.self_harm_result:
        categories["SelfHarm"] = {"severity": response.self_harm_result.severity, "detected": response.self_harm_result.severity > 0}
    if response.sexual_result:
        categories["Sexual"] = {"severity": response.sexual_result.severity, "detected": response.sexual_result.severity > 0}
    if response.violence_result:
        categories["Violence"] = {"severity": response.violence_result.severity, "detected": response.violence_result.severity > 0}

    return {"categories": categories}

def create_text_analysis_request(text: str) -> Dict[str, Any]:
    """
    Creates a text analysis request payload for Azure AI Content Safety.
    """
    return {"text": text}
