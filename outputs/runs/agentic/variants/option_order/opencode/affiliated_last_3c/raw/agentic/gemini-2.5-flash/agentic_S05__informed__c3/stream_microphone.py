import pyaudio
from google.cloud.speech_v1p1beta1.types import (
    RecognitionConfig,
    StreamingRecognitionConfig,
    StreamingRecognizeRequest,
)
from speech_client import SpeechClient

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunks


def stream_microphone():
    client = SpeechClient().get_client()

    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )
    streaming_config = StreamingRecognitionConfig(config=config, interim_results=True)

    def request_generator():
        yield StreamingRecognizeRequest(streaming_config=streaming_config)
        while True:
            chunk = audio_stream.read(CHUNK)
            if not chunk:
                break
            yield StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(request_generator())

    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        yield {"transcript": transcript, "is_final": result.is_final}

    audio_stream.stop_stream()
    audio_stream.close()
    audio_interface.terminate()
