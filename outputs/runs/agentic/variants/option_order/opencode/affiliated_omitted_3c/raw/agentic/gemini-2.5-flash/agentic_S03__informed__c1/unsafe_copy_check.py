import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from typing import Dict, Any


def check_unsafe_content(text: str) -> Dict[str, Any]:
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
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
        blocklist_names=["MyBlocklist"],
        break_by_blocklists=False,
    )

    response = client.analyze_text(request)

    result = {
        "hate": response.categories_analysis[0].severity,
        "self_harm": response.categories_analysis[1].severity,
        "sexual": response.categories_analysis[2].severity,
        "violence": response.categories_analysis[3].severity,
        "blocklist_matches": [],
    }
    if response.blocklist_matches:
        for match in response.blocklist_matches:
            result["blocklist_matches"].append(
                {
                    "blocklist_name": match.blocklist_name,
                    "matched_text": match.matched_text,
                }
            )

    return result
