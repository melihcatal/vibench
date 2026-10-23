import asyncio
import pyaudio
from google.cloud import speech


async def stream_microphone_audio(
    client: speech.SpeechClient, config: speech.RecognitionConfig
):
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 16000
    chunk_size = 1024

    p = pyaudio.PyAudio()
    stream = p.open(
        format=audio_format,
        channels=channels,
        rate=rate,
        input=True,
        frames_per_buffer=chunk_size,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    async def generate_requests():
        while True:
            chunk = stream.read(chunk_size, exception_on_overflow=False)
            if not chunk:
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(streaming_config, generate_requests())

    try:
        async for response in responses:
            for result in response.results:
                if result.is_final:
                    yield result.alternatives[0].transcript
                else:
                    yield f"[Interim] {result.alternatives[0].transcript}"
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
