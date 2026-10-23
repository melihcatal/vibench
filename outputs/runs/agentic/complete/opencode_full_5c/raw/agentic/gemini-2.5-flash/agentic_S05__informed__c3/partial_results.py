import asyncio
from google.cloud import speech


async def handle_speech_recognition_events(responses):
    async for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        is_final = result.is_final

        if is_final:
            yield {"type": "final", "transcript": transcript}
        else:
            yield {"type": "partial", "transcript": transcript}
