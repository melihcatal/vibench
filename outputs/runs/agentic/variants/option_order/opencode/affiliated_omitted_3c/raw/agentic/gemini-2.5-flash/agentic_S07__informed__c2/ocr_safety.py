import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential


def ocr_safety(text: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables"
        )

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    # Default categories to check
    # request.categories = [
    #     TextCategory.HATE,
    #     TextCategory.SELF_HARM,
    #     TextCategory.SEXUAL,
    #     TextCategory.VIOLENCE,
    # ]
    # request.blocklist_names = ["myblocklist"]
    # request.break_by_blocklists = True

    response = client.analyze_text(request)

    safety_results = {
        "hate": response.categories_analysis[0].severity
        if response.categories_analysis
        else 0,
        "self_harm": response.categories_analysis[1].severity
        if response.categories_analysis
        else 0,
        "sexual": response.categories_analysis[2].severity
        if response.categories_analysis
        else 0,
        "violence": response.categories_analysis[3].severity
        if response.categories_analysis
        else 0,
    }
    return safety_results
