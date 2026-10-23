# speech_models.py
from typing import List, Dict, Any


class TranscriptionRequest:
    def __init__(self, audio_path: str, language: str = "en-US"):
        self.audio_path = audio_path
        self.language = language


class TranscriptionResponse:
    def __init__(self, job_id: str, status: str):
        self.job_id = job_id
        self.status = status


class TranscriptResult:
    def __init__(self, results: List[Dict[str, Any]]):
        self.results = results

    @property
    def text(self) -> str:
        return "".join([seg["text"] for seg in self.results if "text" in seg])


class DiarizationConfig:
    def __init__(self, speaker_count: int = 2):
        self.speaker_count = speaker_count


class TimestampedWord:
    def __init__(self, word: str, start: float, end: float):
        self.word = word
        self.start = start
        self.end = end
