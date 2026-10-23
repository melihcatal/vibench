from document_client import get_content_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions

def check_for_unsafe_content(text: str) -> dict:
    client = get_content_safety_client()

    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    # The response object will contain categories like Hate, SelfHarm, Sexual, Violence and their severities
    # We can convert this into a dictionary for easier consumption.
    safety_results = {
        "hate": {"severity": response.hate_result.severity if response.hate_result else 0},
        "self_harm": {"severity": response.self_harm_result.severity if response.self_harm_result else 0},
        "sexual": {"severity": response.sexual_result.severity if response.sexual_result else 0},
        "violence": {"severity": response.violence_result.severity if response.violence_result else 0},
    }
    
    return safety_results
