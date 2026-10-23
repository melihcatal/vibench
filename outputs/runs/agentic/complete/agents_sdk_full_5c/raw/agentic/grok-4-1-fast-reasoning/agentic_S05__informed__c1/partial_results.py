import asyncio
from deepgram import LiveTranscriptionEvents
from typing import AsyncGenerator

async def handle_partial_results(connection) -> AsyncGenerator[str, None]:
    """
    Handles partial and final streaming recognition events from Deepgram connection.
    Yields formatted partial and final transcripts.
    """
    queue = asyncio.Queue()

    def on_transcript_event(transcript):
        asyncio.create_task(queue.put(transcript))

    connection.on(LiveTranscriptionEvents.Transcript, on_transcript_event)

    try:
        while True:
            transcript = await queue.get()
            alternative = transcript.channel.alternatives[0]
            text = alternative.transcript.strip()
            if text:
                if hasattr(transcript, 'is_final') and transcript.is_final:
                    yield f"FINAL: {text}"
                else:
                    yield f"PARTIAL: {text}"
    except asyncio.CancelledError:
        pass
