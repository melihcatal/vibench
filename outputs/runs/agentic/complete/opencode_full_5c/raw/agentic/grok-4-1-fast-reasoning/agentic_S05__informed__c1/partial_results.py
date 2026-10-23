import asyncio
from typing import AsyncGenerator
from speech_models import TranscriptChunk
from deepgram.types.live import LiveTranscriptResult
from deepgram import LiveTranscriptionEvents


class PartialResultsHandler:
    def __init__(self):
        self.partial_buffer = ""

    def handle_transcript_event(self, transcript: LiveTranscriptResult, **kwargs):
        if transcript.channel and transcript.channel.alternatives:
            text = transcript.channel.alternatives[0].transcript or ""
            is_final = transcript.is_final
            if is_final:
                final_text = self.partial_buffer + text
                print(f"FINAL TRANSCRIPT: {final_text}")
                self.partial_buffer = ""
            else:
                self.partial_buffer = text  # Progressive partials
                print(f"PARTIAL: {self.partial_buffer}", end="\r")


async def process_partial_results(
    transcripts: AsyncGenerator[TranscriptChunk, None],
) -> AsyncGenerator[TranscriptChunk, None]:
    handler = PartialResultsHandler()
    async for chunk in transcripts:
        # Simulate event handling
        handler.handle_transcript_event(
            LiveTranscriptResult(
                channel=type(
                    "Channel",
                    (),
                    {"alternatives": [type("Alt", (), {"transcript": chunk.text})]},
                )(),
                is_final=chunk.is_final,
            )
        )
        yield chunk
