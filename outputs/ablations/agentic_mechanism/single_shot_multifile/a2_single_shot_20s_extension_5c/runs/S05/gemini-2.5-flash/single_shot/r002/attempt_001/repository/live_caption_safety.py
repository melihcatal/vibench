import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

from speech_models import SafetyResult

AZURE_CS_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CS_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

if not AZURE_CS_ENDPOINT or not AZURE_CS_KEY:
    raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

def check_caption_safety(text: str) -> SafetyResult:
    client = ContentSafetyClient(AZURE_CS_ENDPOINT, AzureKeyCredential(AZURE_CS_KEY))

    # Default values for severity levels are 0. If nothing is explicitly set, all are checked with severity 0.
    # You can set specific severities for each category.
    # For example: hate_category_severity=2
    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE
        ]
    )

    response = client.analyze_text(request)

    category_scores = {
        'Hate': 0,
        'SelfHarm': 0,
        'Sexual': 0,
        'Violence': 0
    }
    
    is_safe = True

    for category_result in response.categories_analysis:
        category_name = category_result.category.value # Access the enum value string
        category_scores[category_name] = category_result.severity
        if category_result.severity > 0: # Assuming any severity above 0 indicates potential unsafe content
            is_safe = False

    return SafetyResult(
        categories=category_scores,
        is_safe=is_safe
    )
