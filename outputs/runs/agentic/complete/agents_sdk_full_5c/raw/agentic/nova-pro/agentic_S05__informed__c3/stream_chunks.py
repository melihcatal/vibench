import io
from google.cloud import speech
from speech_client import get_speech_client
from speech_models import create_streaming_config, normalize_response

# Streams audio chunks from an async source

def stream_chunks(audio_source):
    client = get_speech_client()
    config = create_streaming_config()
    audio_stream = io.BytesIO()
    for chunk in audio_source:
        audio_stream.write(chunk)
        request = speech.StreamingRecognizeRequest(audio_content=chunk)
        responses = client.streaming_recognize(config, [request])
        for transcript in normalize_response(responses):
            yield transcript