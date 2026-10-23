import os
import asyncio
from deepgram import DeepgramClient, DeepgramClientOptions, LiveTranscriptionEvents, LiveOptions

# Deepgram API Key from environment variable
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

async def handle_streaming_recognition(audio_source_generator):
    if DEEPGRAM_API_KEY is None:
        raise ValueError("DEEPGRAM_API_KEY environment variable not set.")

    config: DeepgramClientOptions = DeepgramClientOptions(
        verbose=1,
    )
    deepgram = DeepgramClient(DEEPGRAM_API_KEY, config)

    # Example: use Websocket connection for streaming
    dg_connection = deepgram.listen.asynclive.v("1")

    async def on_message(self, result, **kwargs):
        if result.type == LiveTranscriptionEvents.PartialResult:
            print(f"Partial: {result.channel.alternatives[0].transcript}")
        elif result.type == LiveTranscriptionEvents.FinalResult:
            print(f"Final: {result.channel.alternatives[0].transcript}")

    async def on_metadata(self, metadata, **kwargs):
        print(f"Metadata: {metadata}")

    async def on_speech_started(self, speech_started, **kwargs):
        print(f"Speech Started: {speech_started}")

    async def on_speaker_update(self, speaker_update, **kwargs):
        print(f"Speaker Update: {speaker_update}")

    async def on_close(self, close, **kwargs):
        print(f"Connection Closed")

    async def on_error(self, error, **kwargs):
        print(f"Error: {error}")

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
    dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
    dg_connection.on(LiveTranscriptionEvents.SpeechStarted, on_speech_started)
    dg_connection.on(LiveTranscriptionEvents.SpeakerUpdate, on_speaker_update)
    dg_connection.on(LiveTranscriptionEvents.Close, on_close)
    dg_connection.on(LiveTranscriptionEvents.Error, on_error)

    options: LiveOptions = LiveOptions(
        smart_format=True,
        language="en-US",
        punctuate=True,
        interim_results=True,
    )

    await dg_connection.start(options)

    try:
        async for chunk in audio_source_generator:
            await dg_connection.send(chunk)
    finally:
        await dg_connection.finish()
