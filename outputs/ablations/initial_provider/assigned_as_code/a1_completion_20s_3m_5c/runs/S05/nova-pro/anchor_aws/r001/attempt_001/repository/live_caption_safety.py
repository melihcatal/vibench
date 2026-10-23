import asyncio

from speech_client import get_comprehend_client

async def check_captions_for_safety(captions):
    comprehend_client = get_comprehend_client()
    unsafe_captions = []
    for caption in captions:
        result = await comprehend_client.detect_sentiment(Text=caption, LanguageCode='en')
        if result['Sentiment'] == 'NEGATIVE':
            unsafe_captions.append(caption)
    return unsafe_captions