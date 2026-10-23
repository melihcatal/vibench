import queue
from typing import Iterator

import pyaudio

from speech_client import create_transcribe_streaming_client, load_speech_config
from speech_models import normalize_transcript_event


def microphone_audio_stream(frame_size: int = 1024) -> Iterator[bytes]:
    config = load_speech_config()
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=config.sample_rate_hz, input=True, frames_per_buffer=frame_size)
    try:
        while True:
            yield stream.read(frame_size, exception_on_overflow=False)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


def stream_microphone():
    config = load_speech_config()
    client = create_transcribe_streaming_client(config.region_name)
    for event in client.start_stream_transcription(
        language_code=config.language_code,
        media_sample_rate_hz=config.sample_rate_hz,
        media_encoding=config.media_encoding,
        audio_stream=microphone_audio_stream(),
    )["TranscriptResultStream"]:
        transcript = normalize_transcript_event(event)
        if transcript.text:
            yield transcript
