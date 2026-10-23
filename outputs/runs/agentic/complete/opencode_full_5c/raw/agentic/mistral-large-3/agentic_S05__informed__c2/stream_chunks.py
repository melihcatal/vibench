import os
from deepgram import Deepgram
import asyncio

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")


async def stream_chunks(audio_chunks):
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    dg_connection = await deepgram.transcription.live(
        {
            "punctuate": True,
            "interim_results": True,
            "language": "en-US",
        }
    )

    async def sender():
        try:
            async for chunk in audio_chunks:
                await dg_connection.send(chunk)
        except Exception as e:
            print(f"Sender error: {e}")
        finally:
            await dg_connection.finish()

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
