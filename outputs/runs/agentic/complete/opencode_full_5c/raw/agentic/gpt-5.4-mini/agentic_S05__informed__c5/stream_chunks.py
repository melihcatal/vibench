from typing import AsyncIterable, AsyncIterator

from google.cloud import speech

from speech_client import build_streaming_config, create_client, load_config
from speech_models import SpeechChunk, TranscriptEvent, TranscriptionRequest


async def stream_chunks(source: AsyncIterable[bytes]) -> AsyncIterator[TranscriptEvent]:
    cfg = load_config()
    client = create_client()
    request = TranscriptionRequest(
        language_code=cfg.language_code, enable_punctuation=cfg.enable_punctuation
    )
    recognizer = build_streaming_config(request)

    async def request_iter():
        async for chunk in source:
            yield speech.StreamingRecognizeRequest(
                audio_content=SpeechChunk(audio=chunk).audio
            )

    for response in client.streaming_recognize(recognizer, request_iter()):
        for result in response.results:
            if result.alternatives:
                yield TranscriptEvent(
                    text=result.alternatives[0].transcript, is_final=result.is_final
                )
