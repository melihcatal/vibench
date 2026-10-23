"""
Translate live captions into another language using Amazon Translate.
Uses the same streaming source as stream_chunks.py (Deepgram).
Credentials: DEEPGRAM_API_KEY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import asyncio
import aiohttp
import os
from typing import AsyncIterator

# Helper to fetch language codes supported by Translate (static list or API call)
SUPPORTED_TARGETS = ['es', 'fr', 'de', 'zh']  # example subset

async def translate_chunk(chunk: str, target_lang: str) -> str:
    """Translates a single caption chunk using Amazon Translate."""
    text = chunk.strip()
    if not text:
        return ''
    api_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = 'us-east-1'
    endpoint = f'https://{region}.translate.amazonaws.com'

    async with aiohttp.ClientSession() as session:
        headers = {
            'Authorization': f'AWS4-HMAC-SHA256 Credential={api_key}/{region}/translate/translateText/aws4_request, SignedHeaders=host;x-amz-content-sha256;x-amz-date, Signature={secret}'
        }
        # Deep integration with boto3 signature calculation omitted for brevity
        # Here we use simplified placeholder POST request (in production use boto3 client translate_text)
        payload = {
            'Text': text,
            'SourceLanguageCode': 'en',
            'TargetLanguageCode': target_lang
        }
        async with session.post(endpoint + '/translateText', json=payload, headers=headers, timeout=10) as resp:
            if resp.status != 200:
                raise RuntimeError(f'Amazon Translate error: {resp.status}')
            data = await resp.json()
            return data.get('TranslatedText', '')

async def translate_live(source_async_gen: AsyncIterator[bytes], target_lang: str = 'es') -> AsyncIterator[str]:
    """Yields translated live captions."""
    async for chunk_bytes in source_async_gen:
        chunk_text = chunk_bytes.decode('utf-8', errors='replace')
        translated = await translate_chunk(chunk_text, target_lang)
        print('Translated:', translated)
        yield translated


def get_target_lang() -> str:
    """Selects a language for translation. Prompting user could be added."""
    return 'es'  # default Spanish

if __name__ == '__main__':
    # Example simple async generator mimicking audio chunk source
    async def dummy_audio_source():
        for _ in range(5):
            await asyncio.sleep(0.6)
            yield b'hello world this is a test. '\n    target = get_target_lang()
    asyncio.run(translate_live(dummy_audio_source(), target_lang=target))