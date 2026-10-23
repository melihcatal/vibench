import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_text_claims(text: str) -> dict:
    """Moderates free-text claims using Azure AI Content Safety.

    Args:
        text: The free text claims or notes to moderate.

    Returns:
        A dictionary containing moderation results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set as environment variables."
        )

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # Categories to check: Hate, SelfHarm, Sexual, Violence
    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    try:
        response = client.analyze_text(request)
        results = {
            "hate_severity": response.hate_result.severity
            if response.hate_result
            else 0,
            "self_harm_severity": response.self_harm_result.severity
            if response.self_harm_result
            else 0,
            "sexual_severity": response.sexual_result.severity
            if response.sexual_result
            else 0,
            "violence_severity": response.violence_result.severity
            if response.violence_result
            else 0,
            "full_response": response.as_dict(),  # Provide full response for detailed analysis
        }
        return results
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Example Usage:
    # export AZURE_CONTENT_SAFETY_ENDPOINT="https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com/"
    # export AZURE_CONTENT_SAFETY_KEY="YOUR_API_KEY"

    example_claim_safe = (
        "This is a perfectly normal user claim about their preferences."
    )
    example_claim_unsafe = (
        "I hate this system and everything about it. I want to hurt myself."
    )

    print("Moderating safe claim:")
    print(moderate_text_claims(example_claim_safe))

    print("\nModerating unsafe claim:")
    print(moderate_text_claims(example_claim_unsafe))
