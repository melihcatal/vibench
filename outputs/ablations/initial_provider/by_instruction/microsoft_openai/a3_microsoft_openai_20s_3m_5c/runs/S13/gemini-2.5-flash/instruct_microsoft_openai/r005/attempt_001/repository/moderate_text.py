import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_text(text_content: str):
    """
    Scores user text for unsafe or policy-violating content using Azure Content Safety.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_content)

    try:
        response = client.analyze_text(request)
        safety_results = {
            "hate": response.categories_analysis[0].severity,
            "self_harm": response.categories_analysis[1].severity,
            "sexual": response.categories_analysis[2].severity,
            "violence": response.categories_analysis[3].severity,
        }
        return safety_results
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    test_text = "I will harm myself."
    results = moderate_text(test_text)
    print(f"Moderation results for '{test_text}': {results}")
