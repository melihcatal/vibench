from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential
import os

def record_text_safety(text_content):
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    try:
        request = AnalyzeTextOptions(text=text_content)
        response = client.analyze_text(request)

        # Extracting results for different categories
        safety_results = {
            "hate": response.hate_result.severity if response.hate_result else 0,
            "self_harm": response.self_harm_result.severity if response.self_harm_result else 0,
            "sexual": response.sexual_result.severity if response.sexual_result else 0,
            "violence": response.violence_result.severity if response.violence_result else 0,
        }
        return {'safety_scores': safety_results}
    except Exception as e:
        print(f"Error checking text safety with Azure Content Safety: {e}")
        return {'safety_scores': None, 'error': str(e)}
