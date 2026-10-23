import asyncio
import os
from google.cloud import speech

speech_client = speech.SpeechClient()

async def stream_chunks():
    async for chunk in microphone_stream():
        yield chunk

async def partial_results():
    async for result in streaming_recognize():
        yield result

async def stream_with_language(language_code='en-US'):
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config)
    async for result in streaming_recognize(streaming_config):
        yield result

async def streaming_recognize(config):
    async with speech_client.streaming_recognize(config) as stream:
        async for response in stream:
            yield response

async def microphone_stream():
    import pyaudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024)
    while True:
        data = stream.read(1024)
        if data:
            yield speech.StreamingRecognizeRequest(audio_content=data)
        await asyncio.sleep(0.01)