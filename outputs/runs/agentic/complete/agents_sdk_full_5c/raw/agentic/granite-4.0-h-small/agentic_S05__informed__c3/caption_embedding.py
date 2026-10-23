import asyncio
import json
import aiohttp
import speech_client as sc
import speech_models as sm
from dotenv import load_dotenv

load_dotenv()

# Embedding provider configuration (OpenAI example)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise RuntimeError('Set OPENAI_API_KEY environment variable')

import openai
openai.api_key = OPENAI_API_KEY

async def embed_text(text: str) -> list[float]:
    """Embed a string using OpenAI embeddings API."""
    response = await asyncio.to_thread(openai.Embedding.create,
                                      model='text-embedding-3-large',
                                      input=text)
    return response[0].embedding  # list of floats

async def embed_caption_chunks(audio_source):
    """Stream captions, embed each final chunk and yield embeddings with metadata."""
    embeddings = []
    async for result in sc.stream_chunks(audio_source):
        if not result.get('final'):
            continue
        transcript = result.get('transcript', '').strip()
        if not transcript:
            continue
        embedding = await embed_text(transcript)
        embeddings.append({
            'transcript': transcript,
            'embedding': embedding,
            'timestamp': result.get('timestamp', None)
        })
        print('Embedded chunk of length', len(transcript))
    return embeddings

if __name__ == '__main__':
    # Demo with a local audio file
    import aiofiles
    async def file_audio_source(path):
        async with aiofiles.open(path, 'rb') as f:
            while chunk := await f.read(1024):
                yield chunk
                await asyncio.sleep(0.01)
    embeddings = asyncio.run(embed_caption_chunks(file_audio_source('sample.wav')))
    print('Total embeddings:', len(embeddings))
