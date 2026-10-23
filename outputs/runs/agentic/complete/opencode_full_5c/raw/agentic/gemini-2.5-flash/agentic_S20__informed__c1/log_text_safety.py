import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from typing import List, Dict, Any


def check_log_text_safety_azure(log_message: str) -> Dict[str, Any]:
    """Checks selected log message text for unsafe content using Azure AI Content Safety."""
    # Ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are set
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    categories = [
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
    ]
    analyze_text_options = AnalyzeTextOptions(text=log_message, categories=categories)

    try:
        response = client.analyze_text(analyze_text_options)
        # Convert the response object to a dictionary for easier consumption
        result = {"message": log_message, "ratings": []}
        for category in response.categories_analysis:
            result["ratings"].append(
                {"category": category.category.value, "severity": category.severity}
            )
        return result
    except Exception as e:
        return {
            "message": log_message,
            "error": f"Error checking content safety with Azure AI: {e}",
        }


if __name__ == "__main__":
    # Example usage: Ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are set
    unsafe_message = "This log contains some hate speech and violent threats."
    safe_message = "User 'testuser' successfully logged in at 2023-10-27 11:30:00."

    print("Checking unsafe message:")
    unsafe_result = check_log_text_safety_azure(unsafe_message)
    print(unsafe_result)

    print("\nChecking safe message:")
    safe_result = check_log_text_safety_azure(safe_message)
    print(safe_result)
