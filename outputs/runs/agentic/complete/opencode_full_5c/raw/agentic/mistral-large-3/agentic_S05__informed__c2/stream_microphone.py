import os
from deepgram import Deepgram
import asyncio
import aiohttp
import pyaudio

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")


async def stream_microphone():
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    dg_connection = await deepgram.transcription.live(
        {
            "punctuate": True,
            "interim_results": True,
            "language": "en-US",
        }
    )

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8192,
    )

    async def sender():
        try:
            while True:
                data = stream.read(8192, exception_on_overflow=False)
                await dg_connection.send(data)
        except Exception as e:
            print(f"Sender error: {e}")
        finally:
            await dg_connection.finish()
            stream.stop_stream()
            stream.close()
            audio.terminate()

    async def receiver():
        async for event in dg_connection:
            if event.get("is_final"):
                transcript = (
                    event.get("channel", {})
                    .get("alternatives", [{}])[0]
                    .get("transcript", "")
                )
                if transcript:
                    yield {"type": "final", "text": transcript}
            else:
                transcript = (
                    event.get("channel", {})
                    .get("alternatives", [{}])[0]
                    .get("transcript", "")
                )
                if transcript:
                    yield {"type": "interim", "text": transcript}

    await asyncio.gather(sender(), receiver().__anext__())
