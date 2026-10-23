from typing import Iterator

from openai import OpenAI

from speech_client import create_openai_client, load_speech_settings
from speech_models import TranscriptEvent, normalize_transcript


def stream_with_language(language: str, punctuation: bool = True) -> Iterator[TranscriptEvent]:
    client: OpenAI = create_openai_client()
    settings = load_speech_settings()
    settings.language = language
    settings.punctuation = punctuation
    result = client.audio.transcriptions.create(model=settings.model, file=b"", language=language)
    text = normalize_transcript(getattr(result, "text", ""))
    if text:
        yield TranscriptEvent(text=text, is_final=True, language=language)
