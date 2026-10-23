from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalysisRequest, AnalyzeTextOptions
import os
from typing import Dict, Any

# Initialize Azure AI Content Safety client
endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
client = ContentSafetyClient(endpoint, AzureKeyCredential(key))


def message_safety(text: str) -> Dict[str, Any]:
    """
    Checks message payload text for unsafe content using Azure AI Content Safety.

    Args:
        text: The text to analyze for unsafe content.

    Returns:
        Dict[str, Any]: Analysis results including categories and severity levels.
    """
    request = TextAnalysisRequest(text=text)
    options = AnalyzeTextOptions(
        categories=["Hate", "SelfHarm", "Sexual", "Violence"], break_by_block=False
    )

    response = client.analyze_text(request, options)

    return {
        "categories_analyzed": options.categories,
        "results": [
            {"category": result.category, "severity": result.severity}
            for result in response.categories_analysis
        ],
    }
