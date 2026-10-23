# [SAME-SCENARIO]
# Asynchronously stream audio chunks to Amazon Transcribe Streaming
# Provider: Amazon Transcribe Streaming (AWS SDK boto3)
import asyncio
import boto3
import json
import pyaudio

# AWS credentials are read from environment variables
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION

STREAM_RATE = 16000
STREAM_WIDTH = 2
STREAM_CHANNELS = 1
FRAMES_PER_BUFFER = 1024

boto_client = boto3.client('transcribe')

def read_microphone():
    """Generator that yields raw 16-bit PCM audio frames from the microphone."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=STREAM_CHANNELS,
                    rate=STREAM_RATE,
                    input=True,
                    frames_per_buffer=FRAMES_PER_BUFFER)
    try:
        while True:
            data = stream.read(FRAMES_PER_BUFFER)
            yield data  # raw bytes
    except KeyboardInterrupt:
        print('Microphone stream stopped.')
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

async def stream_to_transcribe(source, stream_arn):
    """Asynchronously send each chunk to Transcribe Streaming."""
    # boto3 client supports send_transcript synchronously; we wrap it with asyncio's executor
    loop = asyncio.get_running_loop()
    for chunk in source:
        # Send chunk (PCM bytes) to AWS
        await loop.run_in_executor(None, boto_client.send_transcript, {'StreamARN': stream_arn, 'Data': chunk})
        # Optional: simulate back‑off or rate limiting here if needed

async def main():
    # Start the streaming transcription job
    response = boto_client.start_stream_transcription(
        LanguageCode='en-US',
        MediaSampleRateHertz=STREAM_RATE,
        MediaEncoding='pcm',
    )
    stream_arn = response['StreamArn']
    print('Stream ARN:', stream_arn)

    async for _ in stream_to_transcribe(read_microphone(), stream_arn):
        pass  # chunks are being sent in the background

if __name__ == '__main__':
    asyncio.run(main())