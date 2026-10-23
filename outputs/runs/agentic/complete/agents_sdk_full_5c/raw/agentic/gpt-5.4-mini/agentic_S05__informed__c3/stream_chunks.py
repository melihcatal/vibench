from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

from speech_client import AzureSpeechStreamingClient
from speech_models import SpeechChunk, StreamingTranscriptEvent


async def stream_chunks(chunks: AsyncIterable[SpeechChunk]) -> AsyncIterator[StreamingTranscriptEvent]:
    client = AzureSpeechStreamingClient()
    recognizer, push_stream = client.recognize_from_push_stream()
    events: list[StreamingTranscriptEvent] = []

    def on_recognizing(evt) -> None:
        events.append(StreamingTranscriptEvent(text=evt.result.text, is_final=False, raw={"provider": "azure-cognitiveservices-speech"}))

    def on_recognized(evt) -> None:
        events.append(StreamingTranscriptEvent(text=evt.result.text, is_final=True, raw={"provider": "azure-cognitiveservices-speech"}))

    recognizer.recognizing.connect(on_recognizing)
    recognizer.recognized.connect(on_recognized)
    recognizer.start_continuous_recognition()
    await client.push_chunks(chunks, push_stream)
    while events:
        yield events.pop(0)
    recognizer.stop_continuous_recognition()
