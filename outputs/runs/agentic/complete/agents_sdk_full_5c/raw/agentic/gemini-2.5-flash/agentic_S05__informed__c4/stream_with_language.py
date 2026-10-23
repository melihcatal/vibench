import asyncio
import os
import boto3
from botocore.exceptions import ClientError
from boto3.session import Session
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent

# Amazon Transcribe Streaming configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1") # Example region

class MyTranscriptResultStreamHandler(TranscriptResultStreamHandler):
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        # This is an example of how to process events.
        # Here, we print transcript segments as they arrive.
        if transcript_event.transcript and transcript_event.transcript.results:
            for result in transcript_event.transcript.results:
                if not result.is_partial:
                    print(f"Final: {result.alternatives[0].transcript}")
                else:
                    print(f"Partial: {result.alternatives[0].transcript}")

async def start_streaming_recognizer(audio_stream_generator, language_code="en-US", enable_punctuation=True):
    session = Session()
    client = session.client("transcribe", region_name=AWS_REGION)
    
    # Using the low-level client for streaming to directly interact with the websocket
    streaming_client = TranscribeStreamingClient(region=AWS_REGION)

    async with streaming_client.websocket_connect(
        language_code=language_code,
        media_sample_rate_hertz=16000,
        media_encoding="pcm",
        enable_automatic_punctuation=enable_punctuation,
    ) as ws:
        # Create a handler to process the transcription events
        handler = MyTranscriptResultStreamHandler(ws.output_stream)

        # Send audio chunks from the generator
        async for chunk in audio_stream_generator:
            await ws.send_audio_event(audio_chunk=chunk)
        
        # Indicate that we are done sending audio
        await ws.end_stream()

        # Start processing the transcription results
        await asyncio.gather(handler.handle_events())
