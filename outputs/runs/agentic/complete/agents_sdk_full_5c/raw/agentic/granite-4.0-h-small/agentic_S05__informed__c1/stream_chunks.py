import asyncio
import json
import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums

# Google Cloud Speech-to-Text Streaming API
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Helper to convert raw audio chunk to protobuf
# Local helper (see speech_models.py) – assumed provided elsewhere
import speech_models  # noqa

async def stream_chunks(audio_source):
    """Streams raw audio chunks to Google Speech streaming recognizer and yields incremental transcripts."""
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    requests = []
    for chunk in audio_source:
        # chunk must be bytes of raw 16kHz linear PCM
        requests.append(speech.StreamingRecognizeRequest(audio_content=chunk))

    # Send streaming requests to server
    responses = client.streaming_recognize(streaming_config, requests)
    for response in responses:
        for result in response.results:
            if result.alternatives:
                transcript = result.alternatives[0].transcript
                print('Transcript:', transcript)
                yield transcript

# Example usage (pseudo async generator for microphone input)
# async def async_microphone_generator():
#     while True:
#         chunk = await read_microphone_chunk()
#         yield chunk

# asyncio.run(stream_chunks(async_microphone_generator()))
