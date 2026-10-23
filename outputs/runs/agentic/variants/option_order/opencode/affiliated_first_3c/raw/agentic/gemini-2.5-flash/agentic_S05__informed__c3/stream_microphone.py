import asyncio
import pyaudio
from google.cloud import speech

from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig

RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunks


async def stream_microphone_audio(config: StreamingRecognitionConfig):
    client = get_speech_client()
    streaming_config = speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=config.language_code,
            enable_automatic_punctuation=config.enable_automatic_punctuation,
        ),
        interim_results=True,
    )

    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    async def request_generator():
        while True:
            chunk = audio_stream.read(CHUNK)
            if not chunk:
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(streaming_config, request_generator())

    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        yield transcript, result.is_final

    audio_stream.stop_stream()
    audio_stream.close()
    audio_interface.terminate()
