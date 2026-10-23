from typing import Optional, List, Dict, Any


class TranscriptionRequest:
    file_url: str
    speaker_diarization: bool
    word_boost: Optional[List[str]] = None
    boost_param: Optional[str] = None

    def __init__(self, file_url: str, speaker_diarization: bool = False):
        self.file_url = file_url
        self.speaker_diarization = speaker_diarization


class TranscriptionResult:
    id: str
    status: str
    text: Optional[str] = None
    words: Optional[List[Dict[str, Any]]] = None
    utterances: Optional[List[Dict[str, Any]]] = None

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.status = kwargs.get("status")
        self.text = kwargs.get("text")
        self.words = kwargs.get("words")
        self.utterances = kwargs.get("utterances")
