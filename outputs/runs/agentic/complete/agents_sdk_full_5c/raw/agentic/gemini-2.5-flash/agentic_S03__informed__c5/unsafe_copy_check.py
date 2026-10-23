import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_unsafe_content(localized_text: str) -> dict:
    """Checks localized copy for unsafe content using Azure AI Content Safety.

    Args:
        localized_text: The text to check for unsafe content.

    Returns:
        A dictionary containing the analysis results.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    categories = [TextCategory.HATE, TextCategory.SEXUAL, TextCategory.SELF_HARM, TextCategory.VIOLENCE]
    request = AnalyzeTextOptions(text=localized_text, categories=categories)
    response = client.analyze_text(request)

    results = {}
    for category_result in response.categories_analysis:
        results[category_result.category.value] = {
            "severity": category_result.severity,
            "is_unsafe": category_result.severity > 0 # A severity of 0 means safe
        }
    return results

if __name__ == '__main__':
    # Example usage (requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY env vars)
    # text_to_check = "I hate you! You are so stupid."
    # safety_results = check_unsafe_content(text_to_check)
    # print(safety_results)
    pass
