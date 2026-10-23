
import asyncio
import os
import time

import boto3

# AWS Transcribe Streaming settings
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_TRANSCRIBE_VOCABULARY_NAME = os.environ.get("AWS_TRANSCRIBE_VOCABULARY_NAME")

# Audio settings - these should match your microphone's output
SAMPLE_RATE = 16000
CHANNELS = 1
BYTES_PER_SAMPLE = 2  # 16-bit audio
FRAME_LENGTH_MS = 100 # milliseconds
CHUNK_SIZE = int(SAMPLE_RATE / (1000 / FRAME_LENGTH_MS)) * BYTES_PER_SAMPLE * CHANNELS

class MicrophoneStream:
    """
    A synchronous iterable that simulates reading audio chunks from a microphone.
    In a real scenario, this would interface with an audio input library like PyAudio.
    """
    def __init__(self, chunk_size):
        self._chunk_size = chunk_size
        print("MicrophoneStream initialized. In a real app, this would capture live audio.")

    def __iter__(self):
        return self

    def __next__(self):
        # Simulate reading a chunk of audio.
        # In a real application, this would be `audio_interface.read(self._chunk_size)`
        # This will block for a short period to simulate real-time audio.
        time.sleep(FRAME_LENGTH_MS / 1000.0)
        # Return silent audio chunk for now.
        # Replace with actual audio data from microphone.
        return b'\x00' * self._chunk_size

async def stream_microphone_transcripts():
    """
    Streams microphone audio to AWS Transcribe and yields interim transcripts.
    """
    client = boto3.client("transcribe", region_name=AWS_REGION)

    # Prepare the audio stream for AWS Transcribe
    microphone_iterator = MicrophoneStream(CHUNK_SIZE)

    try:
        response = client.start_stream_transcription(
            LanguageCode="en-US", # Example language, should be configurable
            MediaSampleRateHertz=SAMPLE_RATE,
            MediaEncoding="pcm",
            VocabularyName=AWS_TRANSCRIBE_VOCABULARY_NAME if AWS_TRANSCRIBE_VOCABULARY_NAME else None,
            # AudioStream expects an iterable that yields bytes
            AudioStream=(
                {
                    'AudioEvent': {
                        'AudioChunk': chunk
                    }
                }
                for chunk in microphone_iterator
            )
        )

        print("AWS Transcribe streaming started...")

        # Process the synchronous result stream from AWS Transcribe
        for event in response["TranscriptResultStream"]:
            if "TranscriptEvent" in event:
                results = event["TranscriptEvent"]["Transcript"]["Results"]
                for result in results:
                    if result["Alternatives"]:
                        transcript_text = result["Alternatives"][0]["Transcript"]
                        if result["IsPartial"]:
                            yield f"[Interim] {transcript_text}"
                        else:
                            yield transcript_text
            # Allow other async tasks to run if there's a pause in events
            await asyncio.sleep(0.01)

    except Exception as e:
        print(f"Error during transcription: {e}")
        # Optionally, re-raise or yield an error message
        yield f"[ERROR] {e}"

    print("AWS Transcribe streaming finished.")
