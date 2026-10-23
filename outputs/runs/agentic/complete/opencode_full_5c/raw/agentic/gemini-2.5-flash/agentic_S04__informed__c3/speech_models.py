from typing import Optional, List, Dict


class TranscriptionRequest:
    def __init__(
        self,
        audio_url: str,
        diarize: bool = False,
        word_boost: Optional[List[str]] = None,
    ):
        self.audio_url = audio_url
        self.diarize = diarize
        self.word_boost = word_boost


class TranscriptionResult:
    def __init__(
        self,
        id: str,
        status: str,
        text: Optional[str] = None,
        words: Optional[List[Dict]] = None,
        utterances: Optional[List[Dict]] = None,
    ):
        self.id = id
        self.status = status
        self.text = text
        self.words = words
        self.utterances = utterances
