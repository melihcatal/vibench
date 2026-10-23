import asyncio
from typing import Callable
from speech_client import get_speech_client
from deepgram.clients.live.v1 import LiveClient, LiveTranscriptionEvents, LiveOptions
from deepgram.extras import Microphone


async def handle_partial_and_final_results(
    on_partial: Callable[[str], None], on_final: Callable[[str], None]
):
    try:
        deepgram_client = get_speech_client()
        options = LiveOptions(model="nova-2", language="en-US")
        dg_connection: LiveClient = deepgram_client.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if not sentence:
                return

            if result.is_final:
                on_final(sentence)
            else:
                on_partial(sentence)

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        microphone = Microphone(dg_connection.send)
        microphone.start()

        print("Listening for speech. Press Enter to stop.")
        input()

        microphone.finish()
        await dg_connection.finish()

    except Exception as e:
        print(f"An error occurred: {e}")


def print_partial(transcript: str):
    print(f"Partial transcript: {transcript}")


def print_final(transcript: str):
    print(f"Final transcript: {transcript}")


if __name__ == "__main__":
    asyncio.run(handle_partial_and_final_results(print_partial, print_final))
