import asyncio
import os
from dotenv import load_dotenv
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

load_dotenv()


async def handle_partial_and_final_results():
    try:
        deepgram = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))
        dg_connection = deepgram.listen.asynclive.v("1")

        def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if result.is_final:
                print(f"Final transcript: {sentence}")
            else:
                print(f"Partial transcript: {sentence}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            model="nova-2",
            language="en-US",
            interim_results=True,
            utterance_end_ms="1000",
        )
        await dg_connection.start(options)

        # In a real scenario, you would be sending audio data here.
        # For demonstration, we'll just wait.
        print("Listening for audio... (simulated)")
        await asyncio.sleep(10)

        await dg_connection.finish()

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(handle_partial_and_final_results())
