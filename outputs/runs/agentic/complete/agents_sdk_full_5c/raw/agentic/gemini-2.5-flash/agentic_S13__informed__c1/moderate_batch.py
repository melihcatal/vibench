import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from typing import List, Dict

def moderate_batch(texts: List[str]) -> List[Dict]:
    """
    Moderates a batch of user messages and returns per-message decisions using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
    batch_results = []
    for i, text in enumerate(texts):
        try:
            request = AnalyzeTextOptions(text=text)
            response = client.analyze_text(request)
            moderation_results = {
                "text_index": i,
                "original_text": text,
                "categories": {
                    category.category.value: category.severity
                    for category in response.categories_analysis
                }
            }
            batch_results.append(moderation_results)
        except Exception as e:
            batch_results.append({
                "text_index": i,
                "original_text": text,
                "error": str(e)
            })
    return batch_results

if __name__ == '__main__':
    # Example usage
    # Set environment variables AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY
    sample_texts = [
        "I love this product!",
        "You are an idiot and I hope you fail.",
        "Let's discuss our plans for next week."
    ]
    results = moderate_batch(sample_texts)
    for res in results:
        print(res)
