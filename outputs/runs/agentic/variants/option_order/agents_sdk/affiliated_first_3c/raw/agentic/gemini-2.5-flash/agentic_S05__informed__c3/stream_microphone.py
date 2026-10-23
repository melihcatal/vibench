import asyncio
import pyaudio
from google.cloud import speech

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunks

async def stream_microphone_audio(language_code: str = "en-US"):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    audio_interface = pyaudio.PyAudio()
    stream = audio_interface.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("* recording")

    def generator():
        while True:
            data = stream.read(CHUNK)
            yield data

    requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in generator())
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        if not response.results:
            continue
        result = response.results[0]
        if not result.alternatives:
            continue
        transcript = result.alternatives[0].transcript
        yield transcript, result.is_final
