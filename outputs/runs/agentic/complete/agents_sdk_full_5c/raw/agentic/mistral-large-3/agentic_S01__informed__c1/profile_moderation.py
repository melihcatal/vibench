import os
from typing import Dict
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextAnalysisRequest, AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError


def moderate_profile_text(text: str) -> Dict:
    client = ContentSafetyClient(
        endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
        credential=AzureKeyCredential(os.getenv("AZURE_CONTENT_SAFETY_KEY"))
    )
    
    request = TextAnalysisRequest(
        text=text,
        categories=["Hate", "Sexual", "Violence", "SelfHarm"],
        break_by_block=False
    )
    
    try:
        response = client.analyze_text(AnalyzeTextOptions(request))
        return {
            "is_approved": all(
                result.severity <= 2 for result in response.categories_analysis
            ),
            "results": [
                {
                    "category": result.category,
                    "severity": result.severity
                } for result in response.categories_analysis
            ]
        }
    except AzureError as e:
        raise Exception(f"Content moderation failed: {str(e)}")