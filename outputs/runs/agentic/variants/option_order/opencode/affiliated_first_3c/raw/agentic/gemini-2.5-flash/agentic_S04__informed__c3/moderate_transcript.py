import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_transcript_text(text: str) -> dict:
    """
    Moderates transcript text using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE_SPEECH,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
        blocklist_names=["Default"],
    )

    response = client.analyze_text(request)

    result = {"moderation_results": []}
    for category_result in response.categories_analysis:
        result["moderation_results"].append(
            {
                "category": category_result.category.value,
                "severity": category_result.severity,
            }
        )

    if response.blocklists_match:
        result["blocklist_matches"] = [
            {"blocklist_name": match.blocklist_name, "matched_text": match.matched_text}
            for match in response.blocklists_match
        ]

    return result
