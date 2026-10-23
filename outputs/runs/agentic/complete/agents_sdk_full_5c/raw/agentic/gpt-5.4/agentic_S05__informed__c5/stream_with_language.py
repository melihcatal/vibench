from __future__ import annotations

from deepgram import LiveTranscriptionEvents

from speech_client import DeepgramStreamingHelper


async def start_streaming_recognizer(
    *,
    language_code: str = "en-US",
    punctuate: bool = True,
    model: str = "nova-2",
):
    helper = DeepgramStreamingHelper()
    connection = await helper.open_connection(
        language=language_code,
        punctuate=punctuate,
        smart_format=punctuate,
        model=model,
    )
    return connection


def attach_basic_logging(connection: object, callback):
    async def on_transcript(_: object, result: object, **__: object) -> None:
        callback(result)

    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)
    return connection
