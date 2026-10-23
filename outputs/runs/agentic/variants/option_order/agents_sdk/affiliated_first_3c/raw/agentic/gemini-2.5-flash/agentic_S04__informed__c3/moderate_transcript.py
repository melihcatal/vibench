import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_text(text: str):
    """Moderates text using Azure AI Content Safety."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    # You can specify categories and their severities here if needed
    # For example: request.categories = [TextCategory.Hate, TextCategory.SelfHarm]

    response = client.analyze_text(request)

    results = {}
    for category_result in response.categories_analysis:
        results[category_result.category.value] = category_result.severity

    return results

if __name__ == '__main__':
    # Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables
    # For example: export AZURE_CONTENT_SAFETY_ENDPOINT="https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com/"
    #              export AZURE_CONTENT_SAFETY_KEY="YOUR_API_KEY"
    example_text_1 = "I hate this! This is terrible and I feel like giving up."
    example_text_2 = "This is a perfectly normal and safe sentence."

    print("Moderating text 1:")
    try:
        moderation_results_1 = moderate_text(example_text_1)
        for category, severity in moderation_results_1.items():
            print(f"  Category: {category}, Severity: {severity}")
    except Exception as e:
        print(f"Error moderating text 1: {e}")

    print("\nModerating text 2:")
    try:
        moderation_results_2 = moderate_text(example_text_2)
        for category, severity in moderation_results_2.items():
            print(f"  Category: {category}, Severity: {severity}")
    except Exception as e:
        print(f"Error moderating text 2: {e}")
