from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextContent
import os

def moderate_batch(texts: list[str]) -> list[dict]:
    """
    Moderates a batch of user messages using Azure Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    results = []
    for text in texts:
        request = AnalyzeTextOptions(text=text)
        try:
            response = client.analyze_text(request)
            categories_analysis = {}
            for category in response.categories_analysis:
                categories_analysis[category.category.value] = {
                    "severity": category.severity,
                    "violated": category.violated,
                }
            results.append({
                "input_text": text,
                "moderation_results": categories_analysis
            })
        except Exception as e:
            results.append({
                "input_text": text,
                "error": str(e)
            })
    return results

if __name__ == '__main__':
    # Set up dummy environment variables for demonstration.
    # In a real scenario, these would be securely configured.
    os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "https://YOUR_AZURE_CONTENT_SAFETY_ENDPOINT.cognitiveservices.azure.com"
    os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_AZURE_CONTENT_SAFETY_KEY"

    batch_texts = [
        "You are an idiot!",
        "Hello, how are you doing today?",
        "I will kill you!"
    ]
    batch_moderation_output = moderate_batch(batch_texts)
    
    print("Batch Moderation Results:")
    for item in batch_moderation_output:
        print(f"  Input: '{item['input_text']}'")
        if "error" in item:
            print(f"    Error: {item['error']}")
        else:
            for category, data in item['moderation_results'].items():
                print(f"    Category: {category}, Violated: {data['violated']}, Severity: {data['severity']}")
