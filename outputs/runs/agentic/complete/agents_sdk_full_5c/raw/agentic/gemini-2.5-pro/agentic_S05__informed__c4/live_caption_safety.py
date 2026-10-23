import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_caption_safety(text: str) -> dict:
    """
    Checks live transcript text for unsafe content using Azure AI Content Safety.

    Args:
        text: The transcript chunk to analyze.

    Returns:
        A dictionary with the analysis results.
    """
    results = {}
    try:
        key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
        endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
        
        client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

        request = AnalyzeTextOptions(text=text)
        
        response = client.analyze_text(request)
        
        results = {
            "hate_severity": response.hate_result.severity if response.hate_result else 0,
            "self_harm_severity": response.self_harm_result.severity if response.self_harm_result else 0,
            "sexual_severity": response.sexual_result.severity if response.sexual_result else 0,
            "violence_severity": response.violence_result.severity if response.violence_result else 0,
        }

    except (KeyError, HttpResponseError) as e:
        print(f"Error during content safety check: {e}")

    return results

if __name__ == '__main__':
    # Ensure AZURE_CONTENT_SAFETY_KEY and AZURE_CONTENT_SAFETY_ENDPOINT are set
    if "AZURE_CONTENT_SAFETY_KEY" in os.environ and "AZURE_CONTENT_SAFETY_ENDPOINT" in os.environ:
        safe_text = "This is a perfectly normal meeting discussion."
        unsafe_text = "This is a hateful and violent statement."

        print(f"Checking safe text: '{safe_text}'")
        safety_result = check_caption_safety(safe_text)
        print(safety_result)
        
        print(f"\nChecking unsafe text: '{unsafe_text}'")
        safety_result_unsafe = check_caption_safety(unsafe_text)
        print(safety_result_unsafe)
    else:
        print("Please set AZURE_CONTENT_SAFETY_KEY and AZURE_CONTENT_SAFETY_ENDPOINT environment variables.")
