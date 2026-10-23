import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_vendor_notes(text_to_moderate: str) -> dict:
    """
    Moderates vendor notes or memo fields using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables not set."
        )

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # Define the categories to analyze
    categories = [
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
    ]

    request = AnalyzeTextOptions(text=text_to_moderate, categories=categories)
    response = client.analyze_text(request)

    moderation_results = {"is_safe": True, "category_scores": {}}

    for category_result in response.categories_analysis:
        moderation_results["category_scores"][category_result.category.value] = {
            "severity": category_result.severity,
            "is_flagged": category_result.severity > 0,  # Severity 0 means no issue
        }
        if category_result.severity > 0:
            moderation_results["is_safe"] = False

    return moderation_results


if __name__ == "__main__":
    # Placeholder for actual usage with AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY set
    if not os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT") or not os.environ.get(
        "AZURE_CONTENT_SAFETY_KEY"
    ):
        print(
            "Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables."
        )
    else:
        sample_note_safe = "Payment for office supplies, all good."
        sample_note_unsafe = "This payment is for some illegal activities."  # Example of potentially unsafe content

        # safe_result = moderate_vendor_notes(sample_note_safe)
        # print("Safe Note Moderation Result:", safe_result)

        # unsafe_result = moderate_vendor_notes(sample_note_unsafe)
        # print("Unsafe Note Moderation Result:", unsafe_result)
        print("Azure AI Content Safety client configured for vendor text moderation.")
