import os
import requests
import json
from speech_models import ModerationResult

def moderate_transcript(text_content: str) -> ModerationResult:
    """Moderates transcript text using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY environment variable not set.")

    api_version = "2023-10-15-preview"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }

    body = {
        "text": text_content,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence"
        ],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels"
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status() # Raise an exception for HTTP errors

    analysis_result = response.json()

    # Determine if content is safe based on severity levels
    is_safe = True
    categories_analysis = {}
    for category in analysis_result.get("categoriesAnalysis", []):
        category_name = category["category"]
        severity = category["severity"]
        categories_analysis[category_name] = severity
        if severity > 0: # Severity > 0 indicates potential unsafe content
            is_safe = False

    return ModerationResult(
        text=text_content,
        is_safe=is_safe,
        categories=categories_analysis
    )

if __name__ == "__main__":
    # Example usage (requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY)
    # os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com/"
    # os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_KEY"
    # 
    # try:
    #     text_to_moderate = "I hate you so much, I want to hurt myself."
    #     moderation_result = moderate_transcript(text_to_moderate)
    #     print(f"Original Text: {moderation_result.text}")
    #     print(f"Is Safe: {moderation_result.is_safe}")
    #     print(f"Categories Analysis: {moderation_result.categories}")
    # 
    #     text_to_moderate_safe = "Hello everyone, welcome to the meeting."
    #     moderation_result_safe = moderate_transcript(text_to_moderate_safe)
    #     print(f"\nOriginal Text: {moderation_result_safe.text}")
    #     print(f"Is Safe: {moderation_result_safe.is_safe}")
    #     print(f"Categories Analysis: {moderation_result_safe.categories}")
    # except Exception as e:
    #     print(f"Error moderating text: {e}")
    pass
