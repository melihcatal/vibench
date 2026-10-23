import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_text(text: str) -> dict:
    """Moderates transcript text using Azure AI Content Safety."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

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

    response = client.analyze_text(request)

    # Process the response to return a summary of moderation results
    moderation_results = {
        "hate": response.hate.severity,
        "self_harm": response.self_harm.severity,
        "sexual": response.sexual.severity,
        "violence": response.violence.severity,
    }
    return moderation_results


if __name__ == "__main__":
    # Example usage
    # text_to_moderate = "I hate you and I will harm myself."
    # moderation_score = moderate_text(text_to_moderate)
    # print(f"Moderation results: {moderation_score}")
    pass
