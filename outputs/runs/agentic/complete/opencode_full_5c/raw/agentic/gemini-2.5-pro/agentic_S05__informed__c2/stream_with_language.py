import asyncio
import os
from dotenv import load_dotenv
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

load_dotenv()


async def stream_with_language_settings(language="en-US", punctuation=True):
    try:
        deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
        if not deepgram_api_key:
            raise ValueError("DEEPGRAM_API_KEY not found in environment variables.")

        deepgram = DeepgramClient(deepgram_api_key)
        dg_connection = deepgram.listen.asynclive.v("1")

        def on_transcript(self, result, **kwargs):
            transcript = result.channel.alternatives[0].transcript
            if transcript:
                print(f"Transcript ({language}): {transcript}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_transcript)

        options = LiveOptions(
            model="nova-2",
            language=language,
            punctuate=punctuation,
        )
        await dg_connection.start(options)

        print(
            f"Started streaming with language '{language}' and punctuation {'enabled' if punctuation else 'disabled'}."
        )
        # Simulate audio streaming for a short duration
        await asyncio.sleep(10)

        await dg_connection.finish()
        print("Streaming finished.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Example: Start streaming with Spanish language and punctuation enabled
    asyncio.run(stream_with_language_settings(language="es", punctuation=True))
