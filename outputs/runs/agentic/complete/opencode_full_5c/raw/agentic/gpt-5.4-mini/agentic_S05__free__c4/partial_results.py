from typing import Iterable, List
from speech_models import TranscriptChunk, join_chunks

class PartialResultHandler:
    def __init__(self) -> None:
        self.partial: List[TranscriptChunk] = []
        self.final: List[TranscriptChunk] = []

    def handle_event(self, event: dict) -> str:
        chunk = TranscriptChunk(text=event.get("text", ""), is_final=bool(event.get("final")))
        if chunk.is_final:
            self.final.append(chunk)
        else:
            self.partial.append(chunk)
        return join_chunks(self.partial + self.final)
