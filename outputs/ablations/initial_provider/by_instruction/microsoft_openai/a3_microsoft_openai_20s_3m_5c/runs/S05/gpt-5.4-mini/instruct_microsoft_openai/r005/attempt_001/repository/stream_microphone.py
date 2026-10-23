import io
from typing import Iterator

import sounddevice as sd
from openai import OpenAI

from speech_client import create_openai_client, load_speech_settings
from speech_models import TranscriptEvent, normalize_transcript


def microphone_audio_chunks(sample_rate: int = 16000, blocksize: int = 3200) -> Iterator[bytes]:
    with sd.RawInputStream(samplerate=sample_rate, blocksize=blocksize, channels=1, dtype="int16") as stream:
        while True:
            data, _ = stream.read(blocksize)
            yield bytes(data)


def stream_microphone() -> Iterator[TranscriptEvent]:
    client: OpenAI = create_openai_client()
    settings = load_speech_settings()
    buffer = io.BytesIO()
    for chunk in microphone_audio_chunks():
        buffer.write(chunk)
        buffer.seek(0)
        result = client.audio.transcriptions.create(model=settings.model, file=buffer)
        text = normalize_transcript(getattr(result, "text", ""))
        if text:
            yield TranscriptEvent(text=text, is_final=False, language=settings.language)
        buffer.seek(0)
        buffer.truncate(0)
