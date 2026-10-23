import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

def check_unsafe_content(translated_texts, threshold=0.7):
    """Check localized copy for unsafe content using Azure Content Safety.",
    Returns list of texts flagged as unsafe.
    """
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
    key = os.getenv('AZURE_CONTENT_SAFETY_KEY')
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    unsafe = []
    for text in translated_texts:
        response = client.analyze_content(content=text, content_type='text')
        # Simple rule: if toxicity score > threshold, flag as unsafe
        if response.safe_content_classification.tXi > threshold:
            unsafe.append(text)
    return unsafe
