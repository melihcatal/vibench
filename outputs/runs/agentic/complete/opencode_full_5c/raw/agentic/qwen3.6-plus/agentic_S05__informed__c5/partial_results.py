import asyncio
from typing import AsyncGenerator, List, Optional, Callable, Awaitable

from speech_models import (
    PartialTranscript,
    FinalTranscript,
    StreamingSpeechResponse,
    normalize_transcript_for_downstream,
)


class PartialResultsHandler:
    def __init__(
        self,
        on_partial: Optional[Callable[[PartialTranscript], Awaitable[None]]] = None,
        on_final: Optional[Callable[[FinalTranscript], Awaitable[None]]] = None,
        on_speech_final: Optional[Callable[[FinalTranscript], Awaitable[None]]] = None,
    ):
        self.on_partial = on_partial
        self.on_final = on_final
        self.on_speech_final = on_speech_final
        self._partial_buffer: List[str] = []
        self._final_transcripts: List[FinalTranscript] = []
        self._current_partial: Optional[PartialTranscript] = None

    async def process_response(self, response: StreamingSpeechResponse) -> None:
        if response.partial:
            self._current_partial = response.partial
            self._partial_buffer.append(response.partial.text)
            if self.on_partial:
                await self.on_partial(response.partial)

        if response.final:
            self._final_transcripts.append(response.final)
            if self.on_final:
                await self.on_final(response.final)

        if response.is_speech_final and response.final:
            if self.on_speech_final:
                await self.on_speech_final(response.final)

    def get_accumulated_text(self) -> str:
        return " ".join(t.text for t in self._final_transcripts)

    def get_final_transcripts(self) -> List[FinalTranscript]:
        return list(self._final_transcripts)

    def get_current_partial(self) -> Optional[PartialTranscript]:
        return self._current_partial

    def reset(self) -> None:
        self._partial_buffer.clear()
        self._final_transcripts.clear()
        self._current_partial = None


async def handle_streaming_results(
    response_stream: AsyncGenerator[StreamingSpeechResponse, None],
    on_partial: Optional[Callable[[PartialTranscript], Awaitable[None]]] = None,
    on_final: Optional[Callable[[FinalTranscript], Awaitable[None]]] = None,
    on_speech_final: Optional[Callable[[FinalTranscript], Awaitable[None]]] = None,
) -> AsyncGenerator[StreamingSpeechResponse, None]:
    handler = PartialResultsHandler(
        on_partial=on_partial,
        on_final=on_final,
        on_speech_final=on_speech_final,
    )

    async for response in response_stream:
        await handler.process_response(response)
        yield response
