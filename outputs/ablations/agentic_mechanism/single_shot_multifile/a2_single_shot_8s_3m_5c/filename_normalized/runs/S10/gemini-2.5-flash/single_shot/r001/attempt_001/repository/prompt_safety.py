from model_client import get_azure_content_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions

def check_content_safety(text: str) -> dict:
    client = get_azure_content_safety_client()
    request = AnalyzeTextOptions(text=text)

    response = client.analyze_text(request)
    
    safety_results = {}
    for category_result in response.categories_analysis:
        safety_results[category_result.category.value.lower()] = {
            "severity": category_result.severity,
            "detected": category_result.severity > 0
        }
    
    return safety_results