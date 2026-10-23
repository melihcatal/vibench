import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from speech_models import ContentSafetyResult

def check_caption_safety(text: str) -> ContentSafetyResult | None:
    """
    Checks live transcript text for unsafe content using Azure AI Content Safety.
    
    Returns a ContentSafetyResult indicating if the text is safe.
    A text is considered unsafe if any category has a severity level > 0.
    """
    try:
        # Get configuration from environment variables
        endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
        key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

        # Create a client
        client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
        
        # Create the request
        request = AnalyzeTextOptions(text=text)

        # Analyze text
        response = client.analyze_text(request)
        
        # Determine if the content is safe
        is_safe = all(r.severity == 0 for r in response.categories_analysis)
        
        details = {
            cat.category.value: cat.severity for cat in response.categories_analysis
        }

        return ContentSafetyResult(text=text, is_safe=is_safe, details=details)

    except KeyError as e:
        print(f"Error: Environment variable {e} not set for Azure Content Safety.")
        return None
    except Exception as e:
        print(f"An error occurred during content safety check: {e}")
        return None
