import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalyzeOptions, TextCategory

def moderate_text(text: str):
    """
    Scores user text for unsafe or policy-violating content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = TextAnalyzeOptions(text=text, categories=[
        TextCategory.HATE_SPEECH,
        TextCategory.VIOLENCE,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM,
    ])

    response = client.analyze_text(request)

    result = {}
    if response.categories_analysis:
        for category in response.categories_analysis:
            result[category.category] = {
                "severity": category.severity,
                "violated": category.violated if hasattr(category, 'violated') else None
            }
    return result

if __name__ == '__main__':
    # Example usage (requires setting environment variables)
    # os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "YOUR_ENDPOINT"
    # os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_KEY"
    #
    # unsafe_text = "I will hurt you."
    # safe_text = "Hello, how are you today?"
    #
    # print(f"Moderation for unsafe text: {moderate_text(unsafe_text)}")
    # print(f"Moderation for safe text: {moderate_text(safe_text)}")
