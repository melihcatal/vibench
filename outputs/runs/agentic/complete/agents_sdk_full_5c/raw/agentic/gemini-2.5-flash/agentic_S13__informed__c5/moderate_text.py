import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalyzeOptions, TextCategory

def moderate_text(text: str):
    """
    Scores user text for unsafe or policy-violating content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = TextAnalyzeOptions(text=text, categories=[
        TextCategory.VIOLENCE,
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM,
    ])

    response = client.analyze_text(request)

    result = {
        "text": text,
        "moderation_results": []
    }
    for category_result in response.categories_analysis:
        result["moderation_results"].append({
            "category": category_result.category.value,
            "severity": category_result.severity
        })
    return result

if __name__ == '__main__':
    # Example usage (requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY to be set)
    # text_to_moderate = "I hate you and want to harm you."
    # moderation_output = moderate_text(text_to_moderate)
    # print(moderation_output)
    pass
