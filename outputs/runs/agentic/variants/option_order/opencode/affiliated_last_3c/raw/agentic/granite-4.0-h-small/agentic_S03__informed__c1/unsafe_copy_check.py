import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

PROVIDER_NAME = os.getenv('PROVIDER_NAME', 'azure_content_safety')
if PROVIDER_NAME != 'azure_content_safety':
    raise ValueError('unsafe_copy_check works only with Azure Content Safety here')

key = os.getenv('AZURE_CONTENT_SAFETY_KEY')
endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def check_unsafe(localized_copy):
    """Check localized copy for unsafe content using Azure AI Content Safety.",
    if not localized_copy:
        return []
    # Send batch request (max 10 per call for demo)
    results = client.analyze_content(localized_copy)[:len(localized_copy)]
    unsafe_items = []
    for idx, result in enumerate(results):
        if result.flagged_content:
            unsafe_items.append({'index': idx, 'details': result.flagged_content})
    return unsafe_items