import asyncio
import os
from deepgram import Deepgram
from dotenv import load_dotenv

load_dotenv()


async def stream_with_language_and_punctuation(
    audio_source, language="en-US", punctuation=True
):
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    if not DEEPGRAM_API_KEY:
        raise ValueError("DEEPGRAM_API_KEY environment variable not set.")

    deepgram = Deepgram(DEEPGRAM_API_KEY)

    dg_connection = deepgram.transcription.live(
        {
            "smart_format": True,
            "interim_results": True,
            "language": language,
            "punctuate": punctuation,
        }
    )

    dg_connection.on(
        "transcriptReceived",
        lambda result: print(
            f"Transcript ({language}): {result.channel.alternatives[0].transcript}"
        ),
    )
    dg_connection.on("error", lambda error: print(f"Deepgram Error: {error}"))

    async for chunk in audio_source:
        await dg_connection.send(chunk)

    await dg_connection.finish()

    yield "Simulated transcript with language and punctuation"
