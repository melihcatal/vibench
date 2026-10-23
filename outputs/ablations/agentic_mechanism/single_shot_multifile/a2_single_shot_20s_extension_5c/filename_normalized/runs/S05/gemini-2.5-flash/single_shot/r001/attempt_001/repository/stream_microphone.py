import os
import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client
from speech_models import create_streaming_recognition_config, create_recognition_config, ENCODING, SAMPLE_RATE_HERTZ, LANGUAGE_CODE

CHUNK = 1024
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1

def stream_microphone_audio():
    client = get_speech_client()

    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(
        format=AUDIO_FORMAT,
        channels=CHANNELS,
        rate=SAMPLE_RATE_HERTZ,
        input=True,
        frames_per_buffer=CHUNK,
    )

    recognition_config = create_recognition_config(
        language_code=LANGUAGE_CODE,
        sample_rate_hertz=SAMPLE_RATE_HERTZ,
        enable_automatic_punctuation=True
    )
    streaming_config = create_streaming_recognition_config(recognition_config)

    def request_generator():
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        while True:
            chunk = audio_stream.read(CHUNK)
            if not chunk:
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    requests = request_generator()
    responses = client.streaming_recognize(requests)

    for response in responses:
        yield response

    audio_stream.stop_stream()
    audio_stream.close()
    audio_interface.terminate()