from speech_client import speech_client
from speech_models import create_streaming_request

# Stream audio chunks from an async source
async def stream_chunks():
    for audio_content in stream_microphone():
        yield create_streaming_request(None, audio_content)