import pyaudio
from typing import AsyncGenerator, Optional

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

from speech_client import (
    create_speech_client,
    build_streaming_config,
    GOOGLE_SPEECH_API_ENDPOINT,
    DEFAULT_MODEL,
)
from speech_models import (
    RecognitionResult,
    normalize_google_response,
    ResultType,
)


SAMPLE_RATE = 16000
CHUNK_DURATION_SEC = 0.1
BYTES_PER_SAMPLE = 2
CHANNELS = 1
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION_SEC)


def create_audio_stream() -> pyaudio.Stream:
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )
    return stream


def audio_generator(
    audio_stream: pyaudio.Stream,
    stop_event=None,
) -> bytes:
    while True:
        if stop_event and stop_event.is_set():
            break
        try:
            data = audio_stream.read(CHUNK_SIZE, exception_on_overflow=False)
            yield data
        except OSError:
            break


async def stream_microphone_transcripts(
    project_id: str,
    language_code: str = "en-US",
    model: str = DEFAULT_MODEL,
    stop_event=None,
) -> AsyncGenerator[RecognitionResult, None]:
    client = create_speech_client()
    config = build_streaming_config(
        project_id=project_id,
        model=model,
        language_code=language_code,
    )

    audio_stream = create_audio_stream()

    def request_generator():
        yield cloud_speech.StreamingRecognizeRequest(
            recognizer=config["recognizer"],
            streaming_config=config["config"],
        )
        for chunk in audio_generator(audio_stream, stop_event):
            yield cloud_speech.StreamingRecognizeRequest(audio=chunk)

    responses = client.streaming_recognize(requests=request_generator())

    for response in responses:
        if response.results:
            result = normalize_google_response(response)
            yield result

    audio_stream.stop_stream()
    audio_stream.close()


async def stream_microphone_with_callback(
    project_id: str,
    on_transcript,
    language_code: str = "en-US",
    model: str = DEFAULT_MODEL,
    stop_event=None,
):
    async for result in stream_microphone_transcripts(
        project_id=project_id,
        language_code=language_code,
        model=model,
        stop_event=stop_event,
    ):
        on_transcript(result)
