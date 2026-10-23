import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalyzeOptions, TextCategory

def moderate_batch(texts: list[str]):
    """
    Moderates a batch of user messages and returns per-message decisions using Azure AI Content Safety.
    Note: Azure AI Content Safety SDK's `analyze_text` processes one text at a time. 
    This function simulates batching by iterating and calling the API for each text.
    For true batching, a custom parallel execution or a service supporting explicit batch endpoints would be needed.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    batch_results = []
    for text in texts:
        request = TextAnalyzeOptions(text=text, categories=[
            TextCategory.HATE_SPEECH,
            TextCategory.VIOLENCE,
            TextCategory.SEXUAL,
            TextCategory.SELF_HARM,
        ])
        response = client.analyze_text(request)

        result = {"text": text, "moderation_results": {}}
        if response.categories_analysis:
            for category in response.categories_analysis:
                result["moderation_results"][category.category] = {
                    "severity": category.severity,
                    "violated": category.violated if hasattr(category, 'violated') else None
                }
        batch_results.append(result)
    return batch_results

if __name__ == '__main__':
    # Example usage (requires setting environment variables)
    # os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "YOUR_ENDPOINT"
    # os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_KEY"
    #
    # batch_of_texts = [
    #     "I hate you and want to hurt you.",
    #     "What a beautiful day to go for a walk.",
    #     "This is a sexually explicit comment."
    # ]
    #
    # print(f"Batch moderation results: {moderate_batch(batch_of_texts)}")
