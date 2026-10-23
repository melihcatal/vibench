import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def check_secret_labels_for_unsafe_text(labels: list, endpoint: str = None, key: str = None) -> list:
    """
    Checks secret labels and notes for unsafe text using Azure Text Analytics.
    
    Args:
        labels: List of secret labels or notes to check.
        endpoint: Azure Text Analytics endpoint. Defaults to AZURE_TEXT_ANALYTICS_ENDPOINT env var.
        key: Azure Text Analytics key. Defaults to AZURE_TEXT_ANALYTICS_KEY env var.
    
    Returns:
        List of unsafe labels with their risk categories.
    """
    if endpoint is None:
        endpoint = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT")
    if key is None:
        key = os.getenv("AZURE_TEXT_ANALYTICS_KEY")
    
    credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    
    documents = [{"id": str(i), "text": label} for i, label in enumerate(labels)]
    response = client.recognize_pii_entities(documents=documents)
    
    unsafe_labels = []
    for doc in response:
        if doc.is_error:
            continue
        if doc.entities:
            unsafe_labels.append({
                "label": labels[int(doc.id)],
                "entities": [entity.category for entity in doc.entities]
            })
    
    return unsafe_labels