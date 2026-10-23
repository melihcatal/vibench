import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

def check_content_safety(text: str):
    """
    Checks extracted document text for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
        safety_results = {}
        for category_result in response.categories:
            safety_results[category_result.category.value] = {
                "severity": category_result.severity,
                "is_safe": category_result.severity == 0 # Severity 0 usually means safe
            }
        return safety_results
    except HttpResponseError as e:
        print(f"Content Safety error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage (requires environment variables set)
    # unsafe_text = "I hate you"
    # safety_report = check_content_safety(unsafe_text)
    # print(f"Safety report for \'{unsafe_text}\' : {safety_report}")

    # safe_text = "Hello, nice to meet you."
    # safety_report = check_content_safety(safe_text)
    # print(f"Safety report for \'{safe_text}\' : {safety_report}")
    pass
