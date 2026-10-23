
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_content_safety(text_to_analyze: str) -> dict:
    """
    Checks text for unsafe content using Azure AI Content Safety.
    Returns a dictionary with the analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials are not set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_to_analyze)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e}")
        return {"error": str(e)}

    results = {
        "Hate": response.hate_result.severity if response.hate_result else 0,
        "SelfHarm": response.self_harm_result.severity if response.self_harm_result else 0,
        "Sexual": response.sexual_result.severity if response.sexual_result else 0,
        "Violence": response.violence_result.severity if response.violence_result else 0,
    }

    return results

if __name__ == '__main__':
    # This is an example, not part of the required functionality.
    if os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT") and os.getenv("AZURE_CONTENT_SAFETY_KEY"):
        unsafe_text = "I hate you and I want to hurt you."
        safety_analysis = check_content_safety(unsafe_text)
        print(f"Analysis for: '{unsafe_text}'")
        print(safety_analysis)

        safe_text = "I love this new product, it's amazing!"
        safety_analysis = check_content_safety(safe_text)
        print(f"Analysis for: '{safe_text}'")
        print(safety_analysis)
