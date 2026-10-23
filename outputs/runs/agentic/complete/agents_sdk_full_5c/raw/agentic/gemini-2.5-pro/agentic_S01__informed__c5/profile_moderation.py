import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from identity_models import ModerationResult

def moderate_profile_text(text_to_moderate: str) -> ModerationResult:
    """
    Moderates profile text using Azure AI Content Safety.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_to_moderate, categories=[
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE
    ])

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return ModerationResult(is_safe=False, details={"error": str(e)})

    details = {}
    is_safe = True
    for category in response.categories_analysis:
        details[category.category.value] = category.severity
        if category.severity > 0:
            is_safe = False

    return ModerationResult(is_safe=is_safe, details=details)
