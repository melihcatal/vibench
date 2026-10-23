from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalyzeRequest, AnalyzeTextOptions
import os
from typing import Dict, List


def check_visual_labels_for_unsafe_text(labels: List[str]) -> Dict[str, Any]:
    """Checks generated visual labels for unsafe text using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    results = []
    for label in labels:
        request = TextAnalyzeRequest(
            text=label,
            categories=["Hate", "SelfHarm", "Sexual", "Violence"],
            break_by_block=False,
        )
        response = client.analyze_text(request)
        results.append(
            {
                "label": label,
                "blocklists_match": response.blocklists_match,
                "categories_analysis": response.categories_analysis,
            }
        )

    return {"results": results}
