from typing import Optional, List


class TranscriptionRequest:
    def __init__(
        self, audio_url: str, diarization: bool = False, word_timestamps: bool = False
    ):
        self.audio_url = audio_url
        self.diarization = diarization
        self.word_timestamps = word_timestamps


class Word:
    def __init__(self, text: str, start: int, end: int):
        self.text = text
        self.start = start
        self.end = end


class Utterance:
    def __init__(self, speaker: str, text: str, words: List[Word]):
        self.speaker = speaker
        self.text = text
        self.words = words


class TranscriptionResult:
    def __init__(
        self,
        id: str,
        status: str,
        text: Optional[str] = None,
        utterances: Optional[List[Utterance]] = None,
    ):
        self.id = id
        self.status = status
        self.text = text
        self.utterances = utterances
