import os
from security_models import ContentSafetyRequest, ContentSafetyResponse
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_payload_safety(request: ContentSafetyRequest) -> ContentSafetyResponse:
    """
    Checks decrypted text for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(api_key))
    
    analysis_request = AnalyzeTextOptions(text=request.text)

    try:
        response = client.analyze_text(analysis_request)
    except HttpResponseError as e:
        print(f"Error analyzing text with Azure Content Safety: {e}")
        raise

    violated_categories = []
    is_safe = True

    if response.hate_result and response.hate_result.severity > 0:
        violated_categories.append(TextCategory.HATE)
        is_safe = False
    if response.self_harm_result and response.self_harm_result.severity > 0:
        violated_categories.append(TextCategory.SELF_HARM)
        is_safe = False
    if response.sexual_result and response.sexual_result.severity > 0:
        violated_categories.append(TextCategory.SEXUAL)
        is_safe = False
    if response.violence_result and response.violence_result.severity > 0:
        violated_categories.append(TextCategory.VIOLENCE)
        is_safe = False

    return ContentSafetyResponse(is_safe=is_safe, violated_categories=[c.value for c in violated_categories])
