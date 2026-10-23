from typing import Any, List

from speech_models import TranscriptResult, normalize_transcript


class PartialResultBuffer:
    def __init__(self) -> None:
        self.partial: List[TranscriptResult] = []
        self.final: List[TranscriptResult] = []

    def handle_event(self, event: Any) -> TranscriptResult:
        result = normalize_transcript(event)
        if result.is_final:
            self.final.append(result)
        else:
            self.partial.append(result)
        return result
