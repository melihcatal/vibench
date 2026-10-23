import asyncio
from typing import AsyncGenerator, Callable, Dict, List, Optional, Tuple

from speech_models import (
    TranscriptResult,
    TranscriptType,
    parse_deepgram_result,
    normalize_transcript_text,
    merge_consecutive_results,
)


class PartialResultHandler:
    def __init__(
        self,
        on_interim: Optional[Callable[[TranscriptResult], None]] = None,
        on_final: Optional[Callable[[TranscriptResult], None]] = None,
        on_utterance_end: Optional[Callable[[List[TranscriptResult]], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
        merge_interim: bool = True,
        min_confidence: float = 0.0,
    ):
        self.on_interim = on_interim
        self.on_final = on_final
        self.on_utterance_end = on_utterance_end
        self.on_error = on_error
        self.merge_interim = merge_interim
        self.min_confidence = min_confidence
        self._interim_buffer: List[TranscriptResult] = []
        self._final_results: List[TranscriptResult] = []
        self._current_interim_text = ""

    def handle_deepgram_response(self, raw_result: dict):
        try:
            result = parse_deepgram_result(raw_result)
            if result.confidence < self.min_confidence and result.confidence > 0:
                return

            if result.is_final:
                self._process_final(result)
            else:
                self._process_interim(result)
        except Exception as e:
            if self.on_error:
                self.on_error(e)

    def _process_interim(self, result: TranscriptResult):
        if self.merge_interim:
            self._interim_buffer.append(result)
            self._current_interim_text = normalize_transcript_text(
                " ".join(r.text for r in self._interim_buffer if r.text)
            )
            merged_interim = TranscriptResult(
                text=self._current_interim_text,
                transcript_type=TranscriptType.INTERIM,
                confidence=result.confidence,
                is_final=False,
                speech_final=False,
                duration=result.duration,
                start_time=result.start_time,
            )
            if self.on_interim:
                self.on_interim(merged_interim)
        else:
            if self.on_interim:
                self.on_interim(result)

    def _process_final(self, result: TranscriptResult):
        self._interim_buffer.clear()
        self._current_interim_text = ""
        self._final_results.append(result)
        if self.on_final:
            self.on_final(result)

    def handle_utterance_end(self):
        if self._interim_buffer and self.on_utterance_end:
            merged = merge_consecutive_results(self._interim_buffer)
            self.on_utterance_end(merged)
            self._interim_buffer.clear()
            self._current_interim_text = ""

    def get_final_transcript(self) -> str:
        return " ".join(r.text for r in self._final_results if r.text.strip())

    def get_all_results(self) -> Tuple[List[TranscriptResult], List[TranscriptResult]]:
        return self._final_results, self._interim_buffer

    def reset(self):
        self._interim_buffer.clear()
        self._final_results.clear()
        self._current_interim_text = ""


async def process_streaming_results(
    result_queue: asyncio.Queue,
    handler: PartialResultHandler,
    stop_event: Optional[asyncio.Event] = None,
) -> AsyncGenerator[TranscriptResult, None]:
    output_queue: asyncio.Queue = asyncio.Queue()

    def emit_result(result: TranscriptResult):
        output_queue.put_nowait(result)

    handler.on_interim = lambda r: emit_result(r)
    handler.on_final = lambda r: emit_result(r)

    async def process_loop():
        while stop_event is None or not stop_event.is_set():
            try:
                raw_result = await asyncio.wait_for(result_queue.get(), timeout=0.5)
                handler.handle_deepgram_response(raw_result)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                if handler.on_error:
                    handler.on_error(e)

    process_task = asyncio.create_task(process_loop())

    try:
        while stop_event is None or not stop_event.is_set():
            try:
                result = await asyncio.wait_for(output_queue.get(), timeout=0.5)
                yield result
            except asyncio.TimeoutError:
                continue
    finally:
        process_task.cancel()


def create_deepgram_callback_handler(
    handler: PartialResultHandler,
) -> Callable:
    def on_transcript(self_conn, result, **kwargs):
        handler.handle_deepgram_response(result)

    return on_transcript


def create_utterance_end_handler(
    handler: PartialResultHandler,
) -> Callable:
    def on_utterance_end(self_conn, **kwargs):
        handler.handle_utterance_end()

    return on_utterance_end
