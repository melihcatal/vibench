"""Check message payload text for unsafe content using Azure AI Content Safety."""
import os
from typing import Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError


client = ContentSafetyClient(
    endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("AZURE_CONTENT_SAFETY_KEY"))
)


def check_message_safety(text: str) -> Dict[str, Any]:
    """Check text for unsafe content using Azure AI Content Safety."""
    try:
        response = client.analyze_text(
            request={
                "text": text,
                "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]
            }
        )
        return {
            "is_safe": all(
                result.severity <= 2 for result in response.categories_analysis
            ),
            "results": [
                {
                    "category": result.category,
                    "severity": result.severity
                }
                for result in response.categories_analysis
            ]
        }
    except AzureError as e:
        return {"is_safe": False, "error": str(e)}