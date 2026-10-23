import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential

def check_message_safety(text_content: str) -> dict:
    """Checks message payload text for unsafe content using Azure AI Content Safety.

    Args:
        text_content: The text content from the message payload to check.

    Returns:
        A dictionary containing the analysis results, e.g., severity scores for categories.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_content,
        categories=[TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE],
        output_type="FourSeverityLevels"
    )

    try:
        response = client.analyze_text(request)
        results = {
            "hate_severity": response.hate_result.severity if response.hate_result else 0,
            "self_harm_severity": response.self_harm_result.severity if response.self_harm_result else 0,
            "sexual_severity": response.sexual_result.severity if response.sexual_result else 0,
            "violence_severity": response.violence_result.severity if response.violence_result else 0,
        }
        return results
    except Exception as e:
        return {"error": str(e), "message": "Error analyzing text content safety."}

if __name__ == '__main__':
    # Example usage
    unsafe_text = "I hate you so much. This is violent content."
    safe_text = "Hello, how are you today?"

    print(f"Safety check for unsafe text: {check_message_safety(unsafe_text)}")
    print(f"Safety check for safe text: {check_message_safety(safe_text)}")
