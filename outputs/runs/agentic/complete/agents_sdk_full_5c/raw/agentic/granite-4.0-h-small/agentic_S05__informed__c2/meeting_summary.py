# [LATER-STEP]
# meeting_summary.py
# Summarize live meeting transcription using OpenAI Chat Completion (provider: OpenAI)
import asyncio
import boto3
import os
import json

# Transcription client (credentials via env vars)
#  AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY (for transcribe)
transcribe_client = boto3.client('transcribe')

# OpenAI client (uses OPENAI_API_KEY env var)
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')
MODEL = 'gpt-4o-mini'   # lightweight summarization model

MAX_CHUNK_WORDS = 500   # keep each chunk under token limit

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
        # In real implementation parse JSON and check for 'Results'
        # Here we simulate a single final chunk with mocked transcript
        yield {'transcript': 'The project timeline will be extended by two weeks due to resource constraints. Next steps include final testing and stakeholder review.', 'is_final': True}
        break

async def summarize(chunk: str) -> str:
    """Send a prompt to OpenAI to summarize the provided text."""
    prompt = (
        f'You are a concise meeting summarizer. Summarize the following meeting snippet in 2-3 sentences, preserving action items and key decisions.\n\n{chunk}'
    )
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()

async def main(source_iter):
    async for caption in transcribe_audio(source_iter):
        if caption['is_final']:
            print('[Caption] Final:', caption['transcript'])
            summary = await summarize(caption['transcript'])
            print('[Summary] ', summary)
        else:
            print('[Caption] Interim (discarding):', caption['transcript'])

if __name__ == '__main__':
    # Demo with dummy async source
    async def dummy():
        yield b''
    asyncio.run(main(dummy()))