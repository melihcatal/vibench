import asyncio
from typing import AsyncGenerator
from deepgram import LiveTranscriptionEvents
from speech_models import parse_live_result, Transcript

class PartialResultsHandler:
    def __init__(self, connection):
        self.connection = connection
        self.transcript_queue = asyncio.Queue()
        self._setup_handlers()

    def _setup_handlers(self):
        def on_transcript(result):
            parsed = parse_live_result(result)
            if parsed:
                asyncio.create_task(self.transcript_queue.put(parsed))

        def on_close(_):
            asyncio.create_task(self.transcript_queue.put(None))

        self.connection.on(LiveTranscriptionEvents.Transcript, on_transcript)
        self.connection.on(LiveTranscriptionEvents.Close, on_close)

    async def transcripts(self) -> AsyncGenerator[Transcript, None]:
        while True:
            transcript = await self.transcript_queue.get()
            if transcript is None:
                break
            yield transcript