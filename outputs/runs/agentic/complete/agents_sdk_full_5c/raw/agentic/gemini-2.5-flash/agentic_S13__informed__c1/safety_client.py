import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from typing import Dict, Any

def get_content_safety_client() -> ContentSafetyClient:
    """
    Initializes and returns an Azure AI Content Safety client.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    return ContentSafetyClient(endpoint, AzureKeyCredential(key))

def analyze_text_with_safety(text: str) -> Dict[str, int]:
    """
    Helper function to analyze text using the initialized Content Safety client.
    Returns a dictionary of category severities.
    """
    client = get_content_safety_client()
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
    # export AZURE_CONTENT_SAFETY_ENDPOINT="https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com"
    # export AZURE_CONTENT_SAFETY_KEY="YOUR_API_KEY"
    try:
        client = get_content_safety_client()
        print("Azure AI Content Safety client initialized successfully.")
        sample_text = "This is a test message."
        results = analyze_text_with_safety(sample_text)
        print("Analysis results:", results)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
