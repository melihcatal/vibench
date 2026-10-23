import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_batch(texts: list[str]):
    """
    Moderates a batch of user messages and returns per-message decisions using Azure AI Content Safety.
    Note: Azure AI Content Safety's `analyze_text` API processes one text at a time. For batching, we iterate.
    A true batch API would send multiple texts in one request, but we simulate it by iterating.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    batch_results = []
    for text in texts:
        request = AnalyzeTextOptions(
            text=text,
            categories=[
                TextCategory.HATE,
                TextCategory.SELF_HARM,
                TextCategory.SEXUAL,
                TextCategory.VIOLENCE
            ]
        )

        response = client.analyze_text(request)

        result = {
            "text": text,
            "moderation_scores": {}
        }

        for category_result in response.categories_analysis:
            result["moderation_scores"][category_result.category.value.lower()] = {
                "severity": category_result.severity,
                "blocked": category_result.severity >= 4 # Example threshold
            }
        batch_results.append(result)
    return batch_results

if __name__ == '__main__':
    # Example usage - ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are set
    # messages = [
    #     "I love this product!",
    #     "You are an idiot.",
    #     "This is a test of a very bad word."
    # ]
    # print(moderate_batch(messages))
    pass
