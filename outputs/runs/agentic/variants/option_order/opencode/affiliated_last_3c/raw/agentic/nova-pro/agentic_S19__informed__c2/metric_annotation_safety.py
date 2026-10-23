import os

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextBlocklist, TextBlocklistItem
from azure.core.credentials import AzureKeyCredential

# [LATER-STEP] metric_annotation_safety.py


def check_metric_annotation_safety(text):
    credential = AzureKeyCredential(os.getenv("AZURE_CONTENT_SAFETY_KEY"))
    client = ContentSafetyClient(
        endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"), credential=credential
    )
    blocklist = TextBlocklist(items=[TextBlocklistItem(text="unsafe", id="1")])
    result = client.classify_text(text=text, blocklist=blocklist)
    return result
