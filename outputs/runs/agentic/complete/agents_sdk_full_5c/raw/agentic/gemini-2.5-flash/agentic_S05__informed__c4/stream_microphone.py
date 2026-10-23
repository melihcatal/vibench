import asyncio
import os
import pyaudio
from google.cloud import speech_v1p1beta1 as speech

# Google Cloud Speech-to-Text streaming configuration
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunks

async def stream_microphone_audio():
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    microphone_stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    async def request_generator():
        while True:
            chunk = microphone_stream.read(CHUNK)
            if not chunk:
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    try:
        async for response in client.streaming_recognize(config=streaming_config, requests=request_generator()):
            for result in response.results:
                if result.is_final:
                    yield result.alternatives[0].transcript
                else:
                    yield result.alternatives[0].transcript
    except Exception as e:
        print(f"Error during streaming: {e}")
    finally:
        microphone_stream.stop_stream()
        microphone_stream.close()
