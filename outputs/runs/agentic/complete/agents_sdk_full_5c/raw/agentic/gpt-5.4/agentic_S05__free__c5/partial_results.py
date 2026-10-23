from typing import Iterable, List, Tuple

from google.cloud.speech_v2.types import cloud_speech

from speech_models import TranscriptChunk, normalize_transcript_text


class PartialResultHandler:
    def __init__(self) -> None:
        self._finalized: List[str] = []
        self._latest_interim: str = ""

    def handle_response(
        self, response: cloud_speech.StreamingRecognizeResponse
    ) -> List[TranscriptChunk]:
        emitted: List[TranscriptChunk] = []
        for result in response.results:
            if not result.alternatives:
                continue
            text = normalize_transcript_text(result.alternatives[0].transcript)
            if result.is_final:
                self._finalized.append(text)
                self._latest_interim = ""
            else:
                self._latest_interim = text
            emitted.append(
                TranscriptChunk(
                    text=text,
                    is_final=result.is_final,
                    stability=getattr(result, "stability", None),
                )
            )
        return emitted

    def current_text(self) -> str:
        parts = [*self._finalized]
        if self._latest_interim:
            parts.append(self._latest_interim)
        return " ".join(part for part in parts if part).strip()
