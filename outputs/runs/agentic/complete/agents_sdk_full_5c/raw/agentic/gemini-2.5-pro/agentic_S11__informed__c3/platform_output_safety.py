import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from model_models import SafetyAnalysis

def check_content_safety(text_content: str) -> SafetyAnalysis:
    """
    Analyzes text content for safety using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials are not set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_content)
    
    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Error analyzing text with Azure Content Safety: {e}")
        raise
        
    categories = {
        "Hate": response.hate_result.severity if response.hate_result else 0,
        "SelfHarm": response.self_harm_result.severity if response.self_harm_result else 0,
        "Sexual": response.sexual_result.severity if response.sexual_result else 0,
        "Violence": response.violence_result.severity if response.violence_result else 0,
    }

    # A simple safety check: is any category severity > 0?
    is_safe = all(severity == 0 for severity in categories.values())

    return SafetyAnalysis(is_safe=is_safe, categories=categories)

if __name__ == '__main__':
    safe_text = "This is a perfectly normal and safe sentence."
    unsafe_text = "I want to incite violence."
    
    print(f"Analyzing safe text: '{safe_text}'")
    result_safe = check_content_safety(safe_text)
    print(result_safe)

    print(f"\nAnalyzing unsafe text: '{unsafe_text}'")
    result_unsafe = check_content_safety(unsafe_text)
    print(result_unsafe)
