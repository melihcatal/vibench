import asyncio
import json
import aiohttp
import speech_client as sc
from dotenv import load_dotenv

load_dotenv()

# Perspective API configuration (example for safety checking)
PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')
if not PERSPECTIVE_API_KEY:
    raise RuntimeError('Set PERSPECTIVE_API_KEY environment variable')

API_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

async def assess_toxicity(text: str) -> dict:
    """Call Perspective API to get toxicity score."""
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    headers = {
        'X-Goog-Api-Key': PERSPECTIVE_API_KEY,
        'Content-Type': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=payload, headers=headers) as resp:
            data = await resp.json()
            return data.get('attributeScores', {}).get('TOXICITY', {}).get('summaryScore', {})

async def live_caption_safety(audio_source, safety_threshold=0.7):
    """Stream captions and filter out unsafe content based on toxicity."""
    unsafe_chunks = []
    async for result in sc.stream_chunks(audio_source):
        if not result.get('final'):
            continue
        transcript = result.get('transcript', '')
        if transcript.strip():
            scores = await assess_toxicity(transcript)
            toxicity = scores.get('value')
            if toxicity and toxicity >= safety_threshold:
                unsafe_chunks.append({'text': transcript, 'toxicity': toxicity})
                print('Unsafe: {:.2f} - {}'.format(toxicity, transcript))
            else:
                print('Safe:', transcript)
    return unsafe_chunks

if __name__ == '__main__':
    # Demo with a local audio file (replace with real audio source)
    import aiofiles
    async def file_audio_source(path):
        async with aiofiles.open(path, 'rb') as f:
            while chunk := await f.read(4096):
                yield chunk
                await asyncio.sleep(0.01)
    asyncio.run(live_caption_safety(file_audio_source('sample.wav'), safety_threshold=0.8))
