import os
from azure.ai.contentsafety import ContentSafetyClient, ContentSafetyApiKeyCredential
from azure.ai.contentsafety.models import TextBlocklist, TextBlocklistItem

def moderate_vendor_text(vendor_text):
    client = ContentSafetyClient(
        endpoint=os.getenv('CONTENT_SAFETY_ENDPOINT'),
        credential=ContentSafetyApiKeyCredential(os.getenv('CONTENT_SAFETY_KEY'))
    )
    blocklist = client.get_text_blocklist()
    for item in blocklist.items:
        if item.text in vendor_text:
            return False
    return True