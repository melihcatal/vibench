from observability_client import clients
from typing import List, Dict, Any
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_log_text_safety(log_messages: List[str]) -> List[Dict[str, Any]]:
    """
    Checks selected log message text for unsafe content using Azure Content Safety.
    """
    content_safety_client = clients.azure_content_safety_client
    
    results = []
    for message in log_messages:
        categories = [
            TextCategory.HATE_SPEECH,
            TextCategory.SEXUAL,
            TextCategory.SELF_HARM,
            TextCategory.VIOLENCE,
        ]
        
        try:
            request = AnalyzeTextOptions(text=message, categories=categories)
            response = content_safety_client.analyze_text(request)
            
            safety_result = {
                "message": message,
                "violations": []
            }
            
            for category_result in response.categories_analysis:
                if category_result.severity > 0:
                    safety_result["violations"].append({
                        "category": category_result.category.value,
                        "severity": category_result.severity
                    })
            results.append(safety_result)
        except Exception as e:
            results.append({
                "message": message,
                "error": str(e)
            })
    
    return results
