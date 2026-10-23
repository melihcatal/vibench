import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_prompt_safety(text: str) -> dict:
    endpoint = os.getenv("AZURE_AI_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_AI_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_AI_CONTENT_SAFETY_ENDPOINT and AZURE_AI_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text,
        categories=[TextCategory.HATE, TextCategory.SEXUAL, TextCategory.VIOLENCE, TextCategory.SELF_HARM]
    )

    try:
        response = client.analyze_text(request)
        results = {
            "hate": response.hate_result.severity,
            "sexual": response.sexual_result.severity,
            "violence": response.violence_result.severity,
            "self_harm": response.self_harm_result.severity
        }
        return results
    except Exception as e:
        print(f"Error checking content safety with Azure: {e}")
        return {"error": str(e)}
