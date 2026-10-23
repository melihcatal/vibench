import pyaudio
import io
from google.cloud import speech
from speech_client import get_speech_client
from speech_models import create_streaming_config, normalize_response

# Streams microphone audio and yields interim transcripts

def stream_microphone():
    client = get_speech_client()
    config = create_streaming_config()
    audio_stream = io.BytesIO()
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    print('Listening...')
    while True:
        data = stream.read(1024)
        audio_stream.write(data)
        request = speech.StreamingRecognizeRequest(audio_content=data)
        responses = client.streaming_recognize(config, [request])
        for transcript in normalize_response(responses):
            yield transcript