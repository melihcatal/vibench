import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

def check_text_safety(text_content: str):
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables")

    client = ContentSafetyClient(AZURE_CONTENT_SAFETY_ENDPOINT, AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY))

    request = AnalyzeTextOptions(
        text=text_content,
        categories=[TextCategory.Hate, TextCategory.SelfHarm, TextCategory.Sexual, TextCategory.Violence],
        blocklist_names=["DefaultBlocklist"]
    )

    response = client.analyze_text(request)

    safety_results = {
        "hate_result": response.hate_result.severity if response.hate_result else -1,
        "self_harm_result": response.self_harm_result.severity if response.self_harm_result else -1,
        "sexual_result": response.sexual_result.severity if response.sexual_result else -1,
        "violence_result": response.violence_result.severity if response.violence_result else -1,
        "blocklist_matches": []
    }
    if response.blocklist_matches:
        safety_results["blocklist_matches"] = [match.blocklist_name for match in response.blocklist_matches]

    return safety_results
