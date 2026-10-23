import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client, get_streaming_config
from speech_models import ResponseParser


RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunks


def stream_microphone_audio():
    """Streams audio from the microphone and yields interim transcripts."""
    client = get_speech_client()
    streaming_config = get_streaming_config()
    response_parser = ResponseParser()

    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    def request_generator():
        yield speech.StreamingRecognizeRequest(audio_config=streaming_config)
        while True:
            chunk = audio_stream.read(CHUNK)
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    print("Listening... Press Ctrl+C to stop.")
    responses = client.streaming_recognize(request_generator())

    for transcript in response_parser.parse(responses):
        yield transcript
