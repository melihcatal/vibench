import asyncio
import os
import json
from azure.ai.contentsafety import ContentSafetyClient
from azure.identity import DefaultAzureCredential

# Azure AI Content Safety (reference provider for live unsafe content detection)
CONTENT_SAFETY_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
CONTENT_SAFETY_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')
credential = DefaultAzureCredential()
client = ContentSafetyClient(endpoint=CONTENT_SAFETY_ENDPOINT, credential=credential)

async def detect_unsafe_captions(caption_generator):
    """Check each caption chunk for unsafe content using Azure Content Safety and filter out harmful segments."""
    for caption in caption_generator:
        # Azure expects a ContentSafety request payload containing the text
        response = client.analyze_content(text=caption, category='unsafe-content')
        # The response contains a list of categories and scores
        unsafe = response.categories.get('unsafe-content')
        if unsafe and unsafe['confidence'] > 0.8:
            print('Unsafe content detected; skipping chunk')
        else:
            print('Safe caption:', caption)
            yield caption

# Example async caption source (placeholder)
# async def caption_source():
#     while True:
#         chunk = await fetch_next_caption()
#         yield chunk

# asyncio.run(detect_unsafe_captions(caption_source()))
