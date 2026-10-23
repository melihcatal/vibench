# [LATER-STEP]
# caption_embedding.py
# Embed caption chunks using Amazon Titan Embeddings (provider: AWS Bedrock Runtime)
import asyncio
import boto3
import os
import json
from typing import List, Dict, Any

# Transcription client (credentials via env vars)
#  AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY (for transcribe)
transcribe_client = boto3.client('transcribe')

# Embeddings client (Bedrock Runtime) configured via env vars
#  AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SECRET_ACCESS_KEY
bedrock_client = boto3.client('bedrock-runtime')

EMBEDDING_MODEL_ID = 'amazon.titan-text-express-v1'   # model identifier

async def transcribe_audio(source_iter):
    """Start a streaming transcription and yield final chunks (interim discarded)."""
    resp = transcribe_client.start_stream_transcription(
        LanguageCode='en-US',
        MediaSampleRateHertz=16000,
        MediaEncoding='pcm',
    )
    stream_arn = resp['StreamArn']
    print(f'[Transcribe] Stream ARN: {stream_arn}')

    while True:
        # Placeholder: fetch next result (real usage needs event streaming)
        result = transcribe_client.get_transcription_result(StreamArn=stream_arn)
        if not result:
            await asyncio.sleep(0.1)
            continue
        payload = result['Payload']
        # Demo: use a static text chunk
        yield {'transcript': 'The quick brown fox jumps over the lazy dog. Embed this text for semantic search.', 'is_final': True}
        break

async def embed_text(text: str) -> Dict[str, Any]:
    """Submit a call to Titan Embeddings and return the embedding vector."""
    request_payload = {
        'contentType': 'text/plain',
        'text': text,
        'modelId': EMBEDDING_MODEL_ID,
    }
    # Bedrock Runtime expects a POST with JSON payload
    response = bedrock_client.invoke_model(
        Body=json.dumps(request_payload).encode('utf-8'),
        ModelId=EMBEDDING_MODEL_ID,
    )
    response_json = json.loads(response.get('Body').read().decode('utf-8'))
    # Expected format: {["embeddings": [{"index": 0, "embedding": [0.1, 0.2, ...]}]}]
    embeddings = response_json.get('embeddings', [])
    if not embeddings:
        raise ValueError('No embeddings returned')
    vec = embeddings[0]['embedding']
    return {'text': text, 'embedding': vec}

async def main(source_iter):
    async for caption in transcribe_audio(source_iter):
        if caption['is_final']:
            print('[Caption] Final:', caption['transcript'])
            emb_result = await embed_text(caption['transcript'])
            print('  Embedding shape:', len(emb_result['embedding']))
            print('  Embedding (first 5 dims):', emb_result['embedding'][:5])
        else:
            print('[Caption] Interim (discarding):', caption['transcript'])

if __name__ == '__main__':
    # Demo with a dummy async source that yields nothing special
    async def dummy():
        yield b''
    asyncio.run(main(dummy()))