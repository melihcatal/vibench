import asyncio
from deepgram.clients.live.v1 import LiveClient, LiveTranscriptionEvents
from deepgram.extras import Microphone
from speech_client import get_speech_client


async def stream_microphone():
    try:
        deepgram_client = get_speech_client()
        dg_connection: LiveClient = deepgram_client.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            if result.is_final:
                print(f"Final: {sentence}")
            else:
                print(f"Interim: {sentence}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        microphone = Microphone(dg_connection.send)
        microphone.start()

        input("Press Enter to stop recording...\n\n")

        microphone.finish()
        await dg_connection.finish()

    except Exception as e:
        print(f"Could not open socket: {e}")
        return


if __name__ == "__main__":
    asyncio.run(stream_microphone())
