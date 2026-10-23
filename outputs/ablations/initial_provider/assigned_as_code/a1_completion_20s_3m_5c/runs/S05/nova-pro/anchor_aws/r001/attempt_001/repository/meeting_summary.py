import asyncio

from speech_client import get_comprehend_client

async def summarize_meeting(captions):
    comprehend_client = get_comprehend_client()
    summary = ''
    for caption in captions:
        result = await comprehend_client.detect_key_phrases(Text=caption, LanguageCode='en')
        summary += ' '.join([phrase['Text'] for phrase in result['KeyPhrases']]) + ' '
    return summary.strip()