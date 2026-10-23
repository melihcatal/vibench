from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
import os


def log_text_safety(text: str) -> dict:
    """
    Checks log message text for unsafe content using Azure AI Content Safety.

    Args:
        text (str): The log message text to check.

    Returns:
        dict: Results of the content safety check.
    """
    if not text:
        return {"error": "No text provided"}

    # Initialize Azure AI Content Safety client
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    try:
        # Analyze text for harmful content
        response = client.analyze_text(
            text_analyze_input={"text": text},
            categories=["Hate", "SelfHarm", "Sexual", "Violence"],
        )

        return {
            "is_safe": all(
                result.severity <= 2 for result in response.categories_analysis
            ),
            "categories": {
                result.category: result.severity
                for result in response.categories_analysis
            },
        }
    except AzureError as e:
        return {"error": f"Azure Content Safety API error: {str(e)}"}
