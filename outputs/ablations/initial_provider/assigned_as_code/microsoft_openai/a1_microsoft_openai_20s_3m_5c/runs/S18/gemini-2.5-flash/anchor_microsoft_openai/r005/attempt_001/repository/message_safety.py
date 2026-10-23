import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential

def check_message_safety(text_content: str, config=None):
    config = config or {}
    endpoint = config.get('endpoint', os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT"))
    key = config.get('key', os.environ.get("AZURE_CONTENT_SAFETY_KEY"))

    if not all([endpoint, key]):
        raise ValueError("Azure Content Safety endpoint and key must be provided.")

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_content,
        categories=[TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE]
    )

    response = client.analyze_text(request)

    safety_results = {
        "hate_score": response.hate.severity,
        "self_harm_score": response.self_harm.severity,
        "sexual_score": response.sexual.severity,
        "violence_score": response.violence.severity,
        "is_safe": all(s.severity == 0 for s in [response.hate, response.self_harm, response.sexual, response.violence])
    }
    return safety_results
