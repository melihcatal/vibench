import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_text_content(text_to_moderate: str) -> dict:
    """
    Moderates text content using Azure AI Content Safety.

    Args:
        text_to_moderate: The text to be analyzed.

    Returns:
        A dictionary containing the moderation analysis results.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials are not set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_to_moderate, categories=[
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE
    ])

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e.reason}")
        return {"error": str(e)}

    results = {
        "hate_result": response.hate_result.severity if response.hate_result else 0,
        "self_harm_result": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual_result": response.sexual_result.severity if response.sexual_result else 0,
        "violence_result": response.violence_result.severity if response.violence_result else 0,
    }
    return results

if __name__ == '__main__':
    transcript_text = "This is a test transcript. It contains some content that needs to be checked for safety."
    moderation_result = moderate_text_content(transcript_text)
    print("Moderation Results:")
    for category, severity in moderation_result.items():
        print(f"  {category}: Severity {severity}")

    harmful_text = "This text contains problematic content that should be flagged."
    moderation_result_harmful = moderate_text_content(harmful_text)
    print("\nModeration Results (Harmful Text):")
    for category, severity in moderation_result_harmful.items():
        print(f"  {category}: Severity {severity}")
