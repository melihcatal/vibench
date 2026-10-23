import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from document_models import SafetyResult


def check_text_safety(text: str) -> SafetyResult:
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(
            f"Analyze text failed. Error code: {e.error.code}, Error message: {e.error.message}"
        )
        return SafetyResult(is_safe=False, violated_categories=["analysis_failed"])

    violated_categories = []
    is_safe = True

    if response.hate_result and response.hate_result.severity > 0:
        is_safe = False
        violated_categories.append("Hate")
    if response.self_harm_result and response.self_harm_result.severity > 0:
        is_safe = False
        violated_categories.append("SelfHarm")
    if response.sexual_result and response.sexual_result.severity > 0:
        is_safe = False
        violated_categories.append("Sexual")
    if response.violence_result and response.violence_result.severity > 0:
        is_safe = False
        violated_categories.append("Violence")

    return SafetyResult(is_safe=is_safe, violated_categories=violated_categories)
