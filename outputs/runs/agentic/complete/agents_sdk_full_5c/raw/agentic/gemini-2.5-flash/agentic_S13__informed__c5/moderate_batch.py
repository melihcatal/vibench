import os
from typing import List, Dict
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalyzeOptions, TextCategory

def moderate_batch(texts: List[str]):
    """
    Moderates a batch of user messages and returns per-message decisions
    using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    batch_results = []
    for text in texts:
        request = TextAnalyzeOptions(text=text, categories=[
            TextCategory.VIOLENCE,
            TextCategory.HATE,
            TextCategory.SEXUAL,
            TextCategory.SELF_HARM,
        ])
        response = client.analyze_text(request)

        per_message_result = {
            "text": text,
            "moderation_results": []
        }
        for category_result in response.categories_analysis:
            per_message_result["moderation_results"].append({
                "category": category_result.category.value,
                "severity": category_result.severity
            })
        batch_results.append(per_message_result)

    return batch_results

if __name__ == '__main__':
    # Example usage (requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY to be set)
    # messages_to_moderate = [
    #     "Hello, how are you?",
    #     "I will hurt you if you don't comply."
    # ]
    # batch_output = moderate_batch(messages_to_moderate)
    # print(batch_output)
    pass
