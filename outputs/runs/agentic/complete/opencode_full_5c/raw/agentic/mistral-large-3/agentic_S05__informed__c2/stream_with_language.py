import os
from deepgram import Deepgram
import asyncio

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")


def get_deepgram_options(
    language: str = "en-US", punctuate: bool = True, interim_results: bool = True
) -> dict:
    return {
        "punctuate": punctuate,
        "interim_results": interim_results,
        "language": language,
    }


async def stream_with_language(
    audio_source, language: str = "en-US", punctuate: bool = True
):
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    options = get_deepgram_options(language, punctuate)

    dg_connection = await deepgram.transcription.live(options)

    async def sender():
        try:
            async for chunk in audio_source:
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
