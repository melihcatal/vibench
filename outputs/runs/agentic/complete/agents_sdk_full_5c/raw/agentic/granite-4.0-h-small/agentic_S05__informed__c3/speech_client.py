import os
from dotenv import load_dotenv
import json

load_dotenv()

# Provider selection via environment variable (example defaults to Google Cloud Speech)
PROVIDER = os.getenv('STT_PROVIDER', 'google')

if PROVIDER == 'google':
    # Google Cloud Speech-to-Text SDK import
    from google.cloud import speech_v1p1beta1 as speech
    # Client initialization
    client = speech.SpeechClient()
    # Requires GOOGLE_APPLICATION_CREDENTIALS env var pointing to service account JSON

def capture_microphone_audio():
    """Yield raw audio frames from microphone using pyaudio or similar."""
    # Placeholder - actual implementation depends on the audio library used
    # This example yields an infinite stream of empty bytes for demonstration
    import time
    while True:
        yield b''  # dummy chunk
        time.sleep(0.01)

def send_streaming_request(audio_chunk):
    """Send an audio chunk to the streaming API and return the raw response."""
    # Construct streaming recognize request for Google Cloud Speech
    if not hasattr(send_streaming_request, 'request'):
        config = speech.StreamingRecognitionConfig(
            config=speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code='en-US',
                enable_automatic_punctuation=True,
            ),
        )
        send_streaming_request.request = speech.StreamingRecognizeRequest(
            streaming_config=config
        )
    # Prepare payload for the request
    payload = {'audio_content': audio_chunk}
    # Convert to the format expected by the SDK (bytes for Google Speech)
    return client.streaming_recognize(send_streaming_request.request, payload)

def parse_partial_results(response_iter):
    """Iterate over streaming response iterator and extract interim transcripts."""
    # Handle iterator of StreamingRecognizeResponse objects
    for response in response_iter:
        for result in response.results:
            if not result.is_final:
                interim = result.alternatives[0].transcript
                print('Interim:', interim)
            else:
                final = result.alternatives[0].transcript
                print('Final:', final)
    return

# Example helper to start streaming recognition
async def start_streaming(config):
    # For Google Speech, streaming_recognize is a blocking call; wrap in asyncio.to_thread
    import asyncio
    response_iter = await asyncio.to_thread(client.streaming_recognize, config)
    parse_partial_results(response_iter)
