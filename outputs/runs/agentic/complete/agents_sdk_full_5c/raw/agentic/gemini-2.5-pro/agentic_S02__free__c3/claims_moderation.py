import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_user_claim(claim_text: str) -> dict:
    """
    Uses Azure Content Safety to moderate a free-text user profile claim.

    Args:
        claim_text: The text from a user profile (e.g., bio, status message).

    Returns:
        A dictionary containing the moderation results.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")
        
    # Create an Azure Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Construct the request
    request = AnalyzeTextOptions(text=claim_text)
    
    try:
        # Analyze text
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Error calling Azure Content Safety API: {e}")
        raise

    results = {
        'hate': response.hate_result.severity if response.hate_result else 0,
        'self_harm': response.self_harm_result.severity if response.self_harm_result else 0,
        'sexual': response.sexual_result.severity if response.sexual_result else 0,
        'violence': response.violence_result.severity if response.violence_result else 0,
    }

    return results

if __name__ == "__main__":
    # Example usage:
    # 1. Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY
    #    environment variables from your Azure resource.
    
    safe_text = "This is my personal profile. I enjoy hiking and reading."
    potentially_unsafe_text = "This text contains potentially problematic content."

    print(f"Moderating safe text: '{safe_text}'")
    safe_results = moderate_user_claim(safe_text)
    print(safe_results)

    print("-" * 20)

    print(f"Moderating potentially unsafe text: '{potentially_unsafe_text}'")
    unsafe_results = moderate_user_claim(potentially_unsafe_text)
    print(unsafe_results)

    # Check if any severity is > 0
    is_flagged = any(severity > 0 for severity in unsafe_results.values())
    print(f"Is the second text flagged? {is_flagged}")
