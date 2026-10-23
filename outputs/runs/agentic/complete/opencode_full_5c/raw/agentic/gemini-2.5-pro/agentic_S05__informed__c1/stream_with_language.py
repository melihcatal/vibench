import asyncio
from deepgram import LiveTranscriptionEvents, LiveOptions
from speech_client import get_deepgram_client


async def stream_with_language_settings(
    language: str = "fr", enable_punctuation: bool = True
):
    """
    Starts a streaming recognizer with specific language and punctuation settings.
    """
    client = get_deepgram_client()

    # Provider-specific options for language and punctuation
    options = LiveOptions(
        model="nova-2",
        language=language,
        punctuate=enable_punctuation,
        encoding="linear16",
        channels=1,
        sample_rate=16000,
    )

    dg_connection = client.listen.asynclive.v("1")

    async def on_message(self, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if transcript:
            print(f"Transcript ({language}): {transcript}")

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    await dg_connection.start(options)

    print(f"Streaming with language='{language}' and punctuate={enable_punctuation}...")
    try:
        await asyncio.sleep(5)  # Keep connection open for demo
    finally:
        await dg_connection.finish()
