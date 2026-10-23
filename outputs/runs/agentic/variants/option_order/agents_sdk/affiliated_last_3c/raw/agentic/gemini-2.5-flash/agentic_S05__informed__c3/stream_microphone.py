import asyncio
from google.cloud import speech
import pyaudio

async def stream_microphone_audio(
    sampling_rate: int = 16000,
    chunk_size: int = 1024,
    language_code: str = "en-US",
):
    """Streams audio from the microphone and yields interim transcripts."""
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sampling_rate,
        language_code=language_code,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sampling_rate,
        input=True,
        frames_per_buffer=chunk_size,
    )

    async def request_generator():
        while True:
            chunk = stream.read(chunk_size)
            if not chunk:
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    requests = request_generator()
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        yield response
