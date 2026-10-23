# [LATER-STEP]
# live_caption_safety.py
# Check live captions for unsafe content using OpenAI Moderation API (provider: OpenAI)
import asyncio
import boto3
import os
import requests

# Provider settings (credentials via env vars)
#   AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY (for transcribe)
#   OPENAI_API_KEY (for moderation)

# Transcription client
transcribe_client = boto3.client('transcribe')
MODERATION_ENDPOINT = 'https://api.openai.com/v1/moderations'
HEADERS = {'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}', 'Content-Type': 'application/json'}

async def transcribe_audio(source_iter):
    """Start streaming transcription and yield interim/final dicts."""
    # For demo we start a job (replace with async SDK in real use)
    resp = transcribe_client.start_stream_transcription(
        LanguageCode='en-US',
        MediaSampleRateHertz=16000,
        MediaEncoding='pcm',
    )
    stream_arn = resp['StreamArn']
    print(f'[Transcribe] Stream ARN: {stream_arn}')

    while True:
        # Placeholder: get next result (implementation should stream events)
        result = transcribe_client.get_transcription_result(StreamArn=stream_arn)
        if not result:
            await asyncio.sleep(0.1)
            continue
        # Simplify to yield a dummy final chunk
        yield {'transcript': 'unsafe content example', 'is_final': True}
        break

async def moderate_text(text: str) -> bool:
    """Call OpenAI moderation endpoint; return True if safe, False if unsafe."""
    payload = {
        'input': text
    }
    response = requests.post(MODERATION_ENDPOINT, headers=HEADERS, json=payload)
    resp_json = response.json()
    # Example structure: resp_json['results'][0]['flagged']
    flagged = resp_json.get('results', [{}])[0].get('flagged')
    if flagged:
        # If any disallowed category appears, treat as unsafe
        unsafe = any(val for val in resp_json.get('results', [{}])[0].get('categories', {}).values() if val)
        return not unsafe
    return True

async def main(source_iter):
    async for caption in transcribe_audio(source_iter):
        if caption['is_final']:
            print('[Caption] Final:', caption['transcript'])
            safe = await moderate_text(caption['transcript'])
            if safe:
                print('  Safe content ✅')
            else:
                print('  Unsafe content detected ❌')
        else:
            print('[Caption] Interim:', caption['transcript'])

if __name__ == '__main__':
    # Demo with a dummy async source that yields one caption
    async def dummy_source():
        yield b'placeholder_audio_bytes'
    asyncio.run(main(dummy_source()))