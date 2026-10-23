import os
import asyncio
import pyaudio
from google.cloud import speech_v1p1beta1 as speech

from speech_client import get_google_speech_client, get_google_streaming_config
from speech_models import TranscriptChunk

CHUNK_SIZE = 1024  # Audio buffer size
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Sample rate

async def stream_microphone_audio():
    client = get_google_speech_client()
    config = get_google_streaming_config("en-US")

    audio_interface = pyaudio.PyAudio()
    stream = audio_interface.open(
        format=AUDIO_FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    # The first request must contain the AudioConfig, subsequent requests must contain audio data.
    yield speech.StreamingRecognizeRequest(streaming_config=config)

    try:
        while True:
            audio_chunk = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            yield speech.StreamingRecognizeRequest(audio_content=audio_chunk)
            await asyncio.sleep(0.01) # Small sleep to yield control
    except Exception as e:
        # Handle stream closure or errors
        pass
    finally:
        stream.stop_stream()
        stream.close()
        audio_interface.terminate()

async def process_microphone_stream():
    recognizer_stream = client.streaming_recognize(requests=stream_microphone_audio())

    async for response in recognizer_stream:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        alternative = result.alternatives[0]
        if alternative.transcript:
            yield TranscriptChunk(
                text=alternative.transcript,
                start_time=result.result_end_time.total_seconds() - alternative.words[0].start_time.total_seconds() if alternative.words else 0.0, # Placeholder, actual start_time needs more logic
                end_time=result.result_end_time.total_seconds(),
                is_final=result.is_final
            )
