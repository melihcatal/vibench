import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_text_claim_with_azure(text_claim: str) -> dict:
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_claim,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e}")
        raise

    return {
        "hate_severity": response.hate_result.severity if response.hate_result else 0,
        "self_harm_severity": response.self_harm_result.severity
        if response.self_harm_result
        else 0,
        "sexual_severity": response.sexual_result.severity
        if response.sexual_result
        else 0,
        "violence_severity": response.violence_result.severity
        if response.violence_result
        else 0,
    }


if __name__ == "__main__":
    user_note = "This is a test note. It is perfectly fine."
    # user_note = "I want to attack the system." # Example of problematic text

    try:
        moderation_result = moderate_text_claim_with_azure(user_note)
        print(f"Moderation results for: '{user_note}'")
        print(moderation_result)

        is_flagged = any(severity > 1 for severity in moderation_result.values())
        if is_flagged:
            print("\nClaim has been flagged for review.")
        else:
            print("\nClaim seems okay.")

    except Exception as e:
        print(f"An error occurred: {e}")
