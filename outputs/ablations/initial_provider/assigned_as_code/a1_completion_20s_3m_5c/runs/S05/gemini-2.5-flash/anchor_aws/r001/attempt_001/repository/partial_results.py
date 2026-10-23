from typing import AsyncIterable

from speech_models import TranscriptSegment


async def partial_results_handler(transcript_segments: AsyncIterable[TranscriptSegment]):
    async for segment in transcript_segments:
        if segment.is_final:
            print(f"Final Transcript: {segment.text}")
        else:
            print(f"Partial Transcript: {segment.text}")
        # In a real application, you might push these results to a queue,
        # a WebSocket, or further processing.
