from safety_client import get_content_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def safety_threshold(text: str, thresholds: dict) -> dict:
    """
    Applies category thresholds to decide whether to allow text based on Azure AI Content Safety results.
    `thresholds` is a dictionary like {"Hate": 2, "Sexual": 4, ...} where the value is the max allowed severity.
    """
    client = get_content_safety_client()
    request = AnalyzeTextOptions(text=text, 
                                 categories=[TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE])
    response = client.analyze_text(request)

    allowed = True
    decision_details = {
        "text": text,
        "allowed": True,
        "violations": []
    }

    if response.hate_result:
        if response.hate_result.severity > thresholds.get("Hate", 0):
            allowed = False
            decision_details["violations"].append({"category": "Hate", "severity": response.hate_result.severity, "threshold": thresholds.get("Hate", 0)})
    if response.self_harm_result:
        if response.self_harm_result.severity > thresholds.get("SelfHarm", 0):
            allowed = False
            decision_details["violations"].append({"category": "SelfHarm", "severity": response.self_harm_result.severity, "threshold": thresholds.get("SelfHarm", 0)})
    if response.sexual_result:
        if response.sexual_result.severity > thresholds.get("Sexual", 0):
            allowed = False
            decision_details["violations"].append({"category": "Sexual", "severity": response.sexual_result.severity, "threshold": thresholds.get("Sexual", 0)})
    if response.violence_result:
        if response.violence_result.severity > thresholds.get("Violence", 0):
            allowed = False
            decision_details["violations"].append({"category": "Violence", "severity": response.violence_result.severity, "threshold": thresholds.get("Violence", 0)})
    
    decision_details["allowed"] = allowed
    return decision_details
