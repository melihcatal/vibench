from __future__ import annotations

from typing import Any

from deepgram.clients.listen.v1.websocket.async_client import AsyncListenWebSocketClient

from speech_models import PartialTranscriptState, TranscriptSegment, deepgram_result_to_segment, normalize_whitespace


class PartialResultsHandler:
    def __init__(self) -> None:
        self.state = PartialTranscriptState()

    def handle_deepgram_message(self, payload: dict[str, Any]) -> TranscriptSegment | None:
        if payload.get("type") != "Results":
            return None
        segment = deepgram_result_to_segment(payload)
        if not segment.text:
            return None
        if segment.is_final:
            self.state.final_segments.append(segment)
            self.state.interim_text = ""
        else:
            self.state.interim_text = normalize_whitespace(segment.text)
        return segment

    @property
    def final_text(self) -> str:
        return " ".join(seg.text for seg in self.state.final_segments).strip()

    @property
    def display_text(self) -> str:
        return self.state.full_text


def attach_partial_result_handlers(
    connection: AsyncListenWebSocketClient,
    handler: PartialResultsHandler,
) -> None:
    @connection.on("Transcript")
    async def _on_transcript(result: dict[str, Any], **_: Any) -> None:
        handler.handle_deepgram_message(result)

    @connection.on("UtteranceEnd")
    async def _on_utterance_end(**_: Any) -> None:
        handler.state.interim_text = ""
