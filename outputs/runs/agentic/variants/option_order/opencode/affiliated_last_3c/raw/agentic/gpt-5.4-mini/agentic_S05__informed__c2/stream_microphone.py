import asyncio

from speech_client import build_deepgram_client, normalize_transcript


async def stream_microphone():
    client = build_deepgram_client()
    stream = client.transcription.live({"punctuate": True, "interim_results": True})
    async for event in stream:
        transcript = (
            event.channel.alternatives[0].transcript
            if event.channel.alternatives
            else ""
        )
        if transcript:
            yield normalize_transcript(transcript)
