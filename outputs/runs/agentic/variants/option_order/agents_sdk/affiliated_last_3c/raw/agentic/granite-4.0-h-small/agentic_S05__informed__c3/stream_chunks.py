# [SAME-SCENARIO] stream_chunks.py
import asyncio
import json
import aiohttp

# Conrete provider: DashScope Real-time ASR
# Uses DashScope SDK (dashscope) for streaming audio chunks

DASHSCOPE_ENDPOINT = 'https://api.dashscope.ai/v1/speech/voice-recognition'
DASHSCOPE_API_KEY = 'DASHSCOPE_API_KEY'  # set via env variable

async def fetch_audio_chunks(url, chunk_generator):
    headers = {
        'Authorization': f'Bearer {DASHSCOPE_API_KEY}',
        'Content-Type': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=next(chunk_generator), headers=headers, timeout=30) as resp:
            if resp.status != 200:
                raise Exception(f'Error {resp.status}: {await resp.text()}')
            async for line in resp.content:
                yield line.decode('utf-8')

async def stream_audio_chunks(audio_source=None):
    # audio_source should be an async iterable yielding bytes
    payload = {"audio_format": "linear16", "language_code": "en-US"}
    url = DASHSCOPE_ENDPOINT
    chunk_gen = iter([payload])  # initial payload
    async for line in fetch_audio_chunks(url, chunk_gen):
        if line.lower().startswith('"partial":'):
            # intermittent partial transcript
            print('Partial:', line.strip())
        elif line.lower().startswith('"result":'):
            # final result event
            print('Result:', line.strip())

if __name__ == '__main__':
    asyncio.run(stream_audio_chunks())