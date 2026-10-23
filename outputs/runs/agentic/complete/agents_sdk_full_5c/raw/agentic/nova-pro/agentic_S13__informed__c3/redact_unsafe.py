import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import Screen, TextBlock
from azure.core.credentials import AzureKeyCredential

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
AZURE_CONTENT_SAFETY_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')

def redact_unsafe(text):
    client = ContentSafetyClient(AZURE_CONTENT_SAFETY_ENDPOINT, AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY))
    screen = Screen(text=text)
    result = client.screen_text(screen)
    redacted_text = text
    for text_block in result.text_blocks:
        if text_block.severity > 0:
            redacted_text = redacted_text[:text_block.start_index] + '*' * (text_block.end_index - text_block.start_index) + redacted_text[text_block.end_index:]
    return redacted_text