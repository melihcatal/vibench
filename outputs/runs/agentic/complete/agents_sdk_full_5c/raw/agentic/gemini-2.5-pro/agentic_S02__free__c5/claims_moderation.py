import os
from dotenv import load_dotenv
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

load_dotenv()

def moderate_user_claim(text_to_moderate: str) -> dict:
    """
    Uses Azure Content Safety to moderate a free-text user profile claim.

    Args:
        text_to_moderate: The string to be analyzed.

    Returns:
        A dictionary containing the moderation results.
    """
    # Get Azure service credentials from environment variables
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not configured.")

    # Create a Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(api_key))

    # Prepare the request
    request = AnalyzeTextOptions(text=text_to_moderate)

    try:
        # Analyze the text
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"HTTP Error during moderation: {e.message}"}

    # Process and return the results
    results = {
        "hate_severity": response.hate_result.severity if response.hate_result else 0,
        "self_harm_severity": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual_severity": response.sexual_result.severity if response.sexual_result else 0,
        "violence_severity": response.violence_result.severity if response.violence_result else 0,
    }

    # Determine overall moderation decision
    is_acceptable = all(severity < 2 for severity in results.values())
    results["is_acceptable"] = is_acceptable

    return results

# Example usage:
# if __name__ == '__main__':
#     user_bio = "This is a normal user biography."
#     moderation_result = moderate_user_claim(user_bio)
#     print(f"Moderating claim: '{user_bio}'")
#     print(f"Result: {moderation_result}")
    
#     problematic_bio = "This is a test with problematic content that violates policies."
#     moderation_result_2 = moderate_user_claim(problematic_bio)
#     print(f"Moderating claim: '{problematic_bio}'")
#     print(f"Result: {moderation_result_2}")
