import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions

from vision_models import ImageLabel


def check_labels_for_safety(labels: list[ImageLabel]) -> dict:
    """Checks detected image labels for harmful text content using Azure Content Safety."""
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    combined_text = ", ".join([label.name for label in labels])

    if not combined_text:
        return {"safe": True, "details": {}}

    request = AnalyzeTextOptions(text=combined_text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"safe": False, "error": str(e)}

    results = {}
    is_safe = True
    for category in response.categories_analysis:
        results[category.category.value] = category.severity
        if category.severity > 0:
            is_safe = False

    return {"safe": is_safe, "details": results}
