import asyncio

from speech_client import get_polly_client

async def embed_captions(captions):
    polly_client = get_polly_client()
    embeddings = []
    for caption in captions:
        result = await polly_client.synthesize_speech(Text=caption, OutputFormat='mp3', VoiceId='Joanna')
        embeddings.append(result['AudioStream'].read())
    return embeddings