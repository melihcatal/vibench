import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_user_bio(bio_text: str) -> dict:
    """
    Moderates a user's free-text bio using Azure AI Content Safety.

    Args:
        bio_text: The user's profile bio text.

    Returns:
        A dictionary with moderation results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=bio_text, categories=[
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
    ])

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"Analyze text failed: {e.response.text}"}

    results = {
        "hate": response.hate_result.severity,
        "self_harm": response.self_harm_result.severity,
        "sexual": response.sexual_result.severity,
        "violence": response.violence_result.severity,
    }
    
    return results

# Example usage:
# if __name__ == '__main__':
#     user_bio = "This is a sample bio expressing opinions."
#     moderation = moderate_user_bio(user_bio)
#     print(f"Moderation results for bio: '{user_bio}'")
#     for category, severity in moderation.items():
#         print(f"  {category.capitalize()}: Severity {severity}")

#     user_bio_toxic = "I want to harm people."
#     moderation_toxic = moderate_user_bio(user_bio_toxic)
#     print(f"Moderation results for bio: '{user_bio_toxic}'")
#     for category, severity in moderation_toxic.items():
#         print(f"  {category.capitalize()}: Severity {severity}")
