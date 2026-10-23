import asyncio
import websockets
import json
import os
import boto3
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# AWS Transcribe Streaming setup
# Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set in your environment variables
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# This is a placeholder for actual audio streaming from a microphone or other source.
# In a real application, you would capture audio and send it as bytes.
async def dummy_audio_stream(chunk_size=1024, num_chunks=10):
    for i in range(num_chunks):
        # Simulate a chunk of audio data (e.g., 16-bit PCM, single channel, 16kHz)
        yield b'\x00' * chunk_size * 2
        await asyncio.sleep(0.2) # Simulate real-time audio

async def stream_with_language(audio_stream_source, language_code="en-US", enable_partial_results_stabilization=True, pii_entity_types="ALL"):
    """
    Starts a streaming recognizer with language and punctuation settings using AWS Transcribe.
    """
    client = boto3.client('transcribe', region_name=AWS_REGION)

    # Generate a pre-signed URL for the Transcribe streaming session
    # Note: This is a simplified approach. For production, consider using sigv4 directly or a more robust SDK method.
    try:
        response = await asyncio.to_thread(client.create_presigned_url, 
            'start_stream_transcription',
            Params={
                'languageCode': language_code,
                'mediaEncoding': 'pcm',
                'sampleRateHertz': 16000,
                'enablePartialResultsStabilization': enable_partial_results_stabilization,
                'partialResultsStability': 'high',
                'piiEntityTypes': pii_entity_types
            },
            ExpiresIn=300, # URL valid for 5 minutes
            HttpMethod='GET'
        )
        websocket_url = response
    except Exception as e:
        print(f"Error creating presigned URL: {e}")
        return

    print(f"Connecting to AWS Transcribe WebSocket: {websocket_url}")

    async with websockets.connect(websocket_url) as websocket:
        async def send_audio():
            async for chunk in audio_stream_source:
                # AWS Transcribe expects audio events to be sent in a specific JSON format
                await websocket.send(json.dumps({
                    'AudioEvent': {
                        'AudioChunk': chunk.decode('latin-1') # Send as base64 encoded string
                    }
                }))
            await websocket.send(json.dumps({'EndOfStream': {}}))

        async def receive_transcripts():
            async for message in websocket:
                data = json.loads(message)
                if "Transcript" in data:
                    transcript_events = data["Transcript"]["Results"]
                    for event in transcript_events:
                        if not event["IsPartial"]:
                            for alt in event["Alternatives"]:
                                yield {"type": "final", "transcript": alt["Transcript"], "language_code": language_code}
                        else:
                            for alt in event["Alternatives"]:
                                yield {"type": "partial", "transcript": alt["Transcript"], "language_code": language_code}

        # Run sending and receiving concurrently
        send_task = asyncio.create_task(send_audio())
        receive_task = asyncio.create_task(receive_transcripts())

        # Yield transcripts as they are received
        async for transcript in receive_task:
            yield transcript

        await send_task # Ensure all audio is sent

if __name__ == "__main__":
    async def main():
        async for transcript_data in stream_with_language(dummy_audio_stream(), language_code="es-ES"):
            print(f"[{transcript_data['type'].upper()}] ({transcript_data['language_code']}): {transcript_data['transcript']}")

    asyncio.run(main())
