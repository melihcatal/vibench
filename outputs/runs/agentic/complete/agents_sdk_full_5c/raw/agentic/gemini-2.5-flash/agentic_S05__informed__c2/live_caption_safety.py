import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential

def check_text_for_safety(text_content: str, endpoint: str, key: str) -> dict:
    """
    Checks the given text for unsafe content using Azure AI Content Safety.

    Args:
        text_content: The text string to analyze.
        endpoint: The Azure Content Safety endpoint URL.
        key: The Azure Content Safety subscription key.

    Returns:
        A dictionary containing the analysis results.
    """
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    categories = [
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE
    ]

    request = AnalyzeTextOptions(text=text_content, categories=categories)
    response = client.analyze_text(request)

    results = {
        "hate_score": next((item.severity for item in response.categories_analysis if item.category == TextCategory.HATE), None),
        "self_harm_score": next((item.severity for item in response.categories_analysis if item.category == TextCategory.SELF_HARM), None),
        "sexual_score": next((item.severity for item in response.categories_analysis if item.category == TextCategory.SEXUAL), None),
        "violence_score": next((item.severity for item in response.categories_analysis if item.category == TextCategory.VIOLENCE), None),
    }
    return results

def live_caption_safety_check(caption_chunk: str) -> dict:
    """
    Performs a safety check on a live caption chunk.
    Requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        print("Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.")
        return {"error": "Azure Content Safety credentials not set"}

    if not caption_chunk.strip():
        return {"message": "Empty caption chunk, skipping safety check.", "scores": {}}

    try:
        safety_scores = check_text_for_safety(caption_chunk, endpoint, key)
        return {"message": "Safety check complete", "scores": safety_scores}
    except Exception as e:
        print(f"Error checking caption safety: {e}")
        return {"error": f"Azure Content Safety API error: {e}", "scores": {}}

if __name__ == "__main__":
    # Set your Azure Content Safety Endpoint and Key
    # os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "YOUR_AZURE_CONTENT_SAFETY_ENDPOINT"
    # os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_AZURE_CONTENT_SAFETY_KEY"

    # example_safe_caption = "The quick brown fox jumps over the lazy dog."
    # result_safe = live_caption_safety_check(example_safe_caption)
    # print(f"Safe Caption: {example_safe_caption}")
    # print(f"Safety Check Result: {result_safe}")

    # example_unsafe_caption = "I hate this! You are so stupid and I will hurt you!"
    # result_unsafe = live_caption_safety_check(example_unsafe_caption)
    # print(f"Unsafe Caption: {example_unsafe_caption}")
    # print(f"Safety Check Result: {result_unsafe}")
    pass
