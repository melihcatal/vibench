import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_corpus_safety_azure(text: str) -> dict:
    """
    Checks the safety of a given text using Azure Content Safety.
    Returns a dictionary of safety analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    try:
        request = AnalyzeTextOptions(text=text)
        response = client.analyze_text(request)

        result = {
            "text": text,
            "categories_analysis": []
        }

        for category in response.categories_analysis:
            result["categories_analysis"].append({
                "category": category.category.value,
                "severity": category.severity
            })
        return result

    except Exception as e:
        print(f"Error checking content safety with Azure: {e}")
        return {"error": str(e), "text": text}
