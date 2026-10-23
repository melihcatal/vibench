
# [LATER-STEP] live_caption_safety.py
import os
import asyncio
import boto3
from speech_client import create_transcribe_streaming_client
from azure_ai_contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

# Provider integrations:
# 1. Amazon Transcribe Streaming (boto3) for live transcription
# 2. Azure AI Content Safety (REST SDK) for unsafe content detection

# Initialize Transcribe client
transcribe_client = create_transcribe_streaming_client()

# Azure Content Safety client (REST) configured via environment variables
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
AZURE_CONTENT_SAFETY_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')
content_safety_client = ContentSafetyClient(endpoint=AZURE_CONTENT_SAFETY_ENDPOINT,
                                             credential=AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY))

UNSAFE_CATEGORIES = ['sexual', 'violence', 'self_harm', 'hate']

async def start_live_caption_and_safety_check():
    # Simulated caption chunks (in practice capture from microphone)
    while True:
        # Placeholder for receiving a new caption chunk
        caption = f"Live caption update {int(os.times()[4])}"
        print('Received caption:', caption)
        # Detect unsafe content using Azure Content Safety API
        poller = content_safety_client.begin_analyze_content(content=caption, content_type='text/plain')
        result = poller.result()
        unsafe = False
        for category, flag in result.unsafe_categories.items():
            if category in UNSAFE_CATEGORIES and flag:
                unsafe = True
                break
        if unsafe:
            print('WARNING: Unsafe content detected. Suppressing output.')
        else:
            print('Safe caption:', caption)
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(start_live_caption_and_safety_check())
