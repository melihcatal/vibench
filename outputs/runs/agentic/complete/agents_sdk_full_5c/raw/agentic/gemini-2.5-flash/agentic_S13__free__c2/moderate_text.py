from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import get_content_safety_client
from safety_models import ModerationResult

def moderate_text(text: str) -> ModerationResult:
    """Scores user text for unsafe or policy-violating content using Azure Content Safety."""
    client = get_content_safety_client()
    request = AnalyzeTextOptions(text=text)
    try:
        response = client.analyze_text(request)
        categories = {}
        for category_analyzer_result in response.categories_analysis:
            categories[category_analyzer_result.category.value] = category_analyzer_result.severity
        return ModerationResult(
            is_safe=all(severity < 2 for severity in categories.values()), # Example threshold
            categories=categories
        )
    except Exception as e:
        print(f"Error moderating text: {e}")
        return ModerationResult(is_safe=False, categories={})

if __name__ == '__main__':
    # This is an example of how to use the function.
    # In a real scenario, you would get API_ENDPOINT and API_KEY from environment variables or a configuration system.
    # Set dummy values for local testing if needed, but they won't work without actual Azure credentials.
    # import os
    # os.environ['AZURE_CONTENT_SAFETY_ENDPOINT'] = "https://your-resource-name.cognitiveservices.azure.com"
    # os.environ['AZURE_CONTENT_SAFETY_KEY'] = "YOUR_AZURE_CONTENT_SAFETY_KEY"

    # result = moderate_text("I hate you! You are ugly.")
    # print(f"Moderation Result: {result.is_safe}, Categories: {result.categories}")

    # result = moderate_text("Hello, how are you?")
    # print(f"Moderation Result: {result.is_safe}, Categories: {result.categories}")
    pass
