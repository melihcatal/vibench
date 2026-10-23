import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_text(text: str):
    """
    Scores user text for unsafe or policy-violating content using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    moderation_results = {
        category.category.value: category.severity
        for category in response.categories_analysis
    }
    return moderation_results

if __name__ == '__main__':
    # Example usage
    # Set environment variables AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY
    # before running.
    # For example:
    # export AZURE_CONTENT_SAFETY_ENDPOINT="https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com"
    # export AZURE_CONTENT_SAFETY_KEY="YOUR_API_KEY"
    sample_text = "I hate this! You are so stupid."
    results = moderate_text(sample_text)
    print("Moderation Results:", results)
