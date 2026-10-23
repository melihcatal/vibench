from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextContentItem
from safety_client import get_content_safety_client
from safety_models import ModerationResult

def moderate_batch(texts: list[str]) -> list[ModerationResult]:
    """Moderates a batch of user messages and returns per-message decisions using Azure Content Safety."""
    client = get_content_safety_client()
    
    # Azure Content Safety doesn't have a direct "batch" API for `analyze_text` with multiple texts in one call
    # for the same document. It's designed per-document.
    # For a batch, we iterate and call the API for each text.
    # For very large batches, consider async calls or a queue-based approach.

    results = []
    for i, text in enumerate(texts):
        request = AnalyzeTextOptions(text=text)
        try:
            response = client.analyze_text(request)
            categories = {}
            for category_analyzer_result in response.categories_analysis:
                categories[category_analyzer_result.category.value] = category_analyzer_result.severity
            results.append(ModerationResult(
                is_safe=all(severity < 2 for severity in categories.values()), # Example threshold
                categories=categories
            ))
        except Exception as e:
            print(f"Error moderating text (item {i}): {e}")
            results.append(ModerationResult(is_safe=False, categories={}))
    return results

if __name__ == '__main__':
    # Example usage (requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY env vars)
    # messages = [
    #     "This is a safe message.",
    #     "I hate you, you are stupid!",
    #     "What a lovely day."
    # ]
    # batch_results = moderate_batch(messages)
    # for i, res in enumerate(batch_results):
    #     print(f"Message {i}: Safe={res.is_safe}, Categories={res.categories}")
    pass
