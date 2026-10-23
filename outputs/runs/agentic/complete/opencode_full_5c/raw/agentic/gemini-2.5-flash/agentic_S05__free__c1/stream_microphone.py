import asyncio
import pyaudio
from google.cloud import speech_v1p1beta1 as speech

from speech_client import get_streaming_config


async def stream_microphone_audio(sampling_rate: int, audio_format: int, channels: int):
    client = speech.SpeechClient()
    streaming_config = get_streaming_config(sampling_rate)

    p = pyaudio.PyAudio()
    stream = p.open(
        format=audio_format,
        channels=channels,
        rate=sampling_rate,
        input=True,
        frames_per_buffer=8192,
    )

    def generate_requests():
        yield speech.StreamingRecognizeRequest(audio_config=streaming_config)
        while True:
            chunk = stream.read(8192)
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(generate_requests())

    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript

    stream.stop_stream()
    stream.close()
    p.terminate()
