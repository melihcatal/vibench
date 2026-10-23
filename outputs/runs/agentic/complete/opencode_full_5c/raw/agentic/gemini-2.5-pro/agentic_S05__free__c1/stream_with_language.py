import asyncio
from speech_client import get_speech_client
from deepgram.clients.live.v1 import LiveClient, LiveTranscriptionEvents, LiveOptions
from deepgram.extras import Microphone


async def stream_with_language_settings():
    try:
        deepgram_client = get_speech_client()

        # Note: Punctuation is enabled by default for 'nova-2' model.
        # Smart format is also a powerful feature for readability.
        options = LiveOptions(
            model="nova-2", language="en-US", punctuate=True, smart_format=True
        )

        dg_connection: LiveClient = deepgram_client.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) > 0:
                print(f"Transcript: {sentence}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        await dg_connection.start(options)

        microphone = Microphone(dg_connection.send)
        microphone.start()

        print("Streaming with language='en-US' and punctuation. Press Enter to stop.")
        input()

        microphone.finish()
        await dg_connection.finish()

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(stream_with_language_settings())
