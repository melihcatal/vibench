from document_client import get_content_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions

def check_text_safety(text: str):
    client = get_content_safety_client()
    
    # Example of analyzing text for safety violations
    # The categories can be configured based on requirements
    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)
    
    safety_results = {
        "hate": response.hate_result.severity if response.hate_result else 0,
        "self_harm": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual": response.sexual_result.severity if response.sexual_result else 0,
        "violence": response.violence_result.severity if response.violence_result else 0,
    }
    
    return safety_results
