from __future__ import annotations

from typing import Iterable, List

from google.cloud import speech

from speech_models import TranscriptSegment, merge_segments


class PartialResultHandler:
    def __init__(self) -> None:
        self._partials: List[str] = []
        self._finals: List[str] = []

    def handle_response(self, response: speech.StreamingRecognizeResponse) -> Iterable[TranscriptSegment]:
        for result in response.results:
            if not result.alternatives:
                continue
            text = result.alternatives[0].transcript
            if result.is_final:
                self._finals.append(text)
                self._partials.clear()
                yield TranscriptSegment(text=text, is_final=True, raw={"partial_count": 0})
            else:
                self._partials.append(text)
                yield TranscriptSegment(text=text, is_final=False, raw={"partial_count": len(self._partials)})

    def current_transcript(self) -> str:
        return merge_segments(TranscriptSegment(text=t, is_final=True) for t in self._finals + self._partials)
