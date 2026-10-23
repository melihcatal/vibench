from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
import os


def secret_label_safety(label: str, notes: str) -> bool:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not configured")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    text = f"Label: {label}\nNotes: {notes}"
    request = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}

    response = client.analyze_text(request)

    return all(result.severity < 2 for result in response.categories_analysis)
