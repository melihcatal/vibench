import os
from vision_client import get_azure_content_safety_client
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_text_for_safety(text_content: str) -> dict:
    client = get_azure_content_safety_client()

    # Categories to check
    categories = [
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM,
        TextCategory.VIOLENCE,
    ]

    request = AnalyzeTextOptions(text=text_content, categories=categories)
    response = client.analyze_text(request)

    safety_results = {}
    for category_result in response.categories_analysis:
        safety_results[category_result.category.value] = category_result.severity

    return safety_results


if __name__ == "__main__":
    # Example usage:
    # Ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are set.
    sample_text = "This is a normal image description."
    safety_scores = check_text_for_safety(sample_text)
    print(f"Text safety scores for '{sample_text}': {safety_scores}")

    unsafe_text = "I hate you all!"
    unsafe_safety_scores = check_text_for_safety(unsafe_text)
    print(f"Text safety scores for '{unsafe_text}': {unsafe_safety_scores}")
