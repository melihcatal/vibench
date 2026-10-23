import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_text(text: str):
    """
    Scores user text for unsafe or policy-violating content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE
        ]
    )

    response = client.analyze_text(request)

    result = {
        "text": text,
        "moderation_scores": {}
    }

    for category_result in response.categories_analysis:
        result["moderation_scores"][category_result.category.value.lower()] = {
            "severity": category_result.severity,
            "blocked": category_result.severity >= 4 # Example threshold
        }
    return result

if __name__ == '__main__':
    # Example usage - ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are set
    # print(moderate_text("I hate you!"))
    # print(moderate_text("This is a normal sentence."))
    pass
