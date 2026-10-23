from typing import List, Dict, Optional, Any

class TranscriptionJob:
    """Represents a submitted transcription job."""
    def __init__(self, job_id: str, status: str):
        self.job_id = job_id
        self.status = status

class TranscriptionResult:
    """Represents the full result of a transcription."""
    def __init__(self, text: str, words: Optional[List[Dict]] = None, utterances: Optional[List[Dict]] = None):
        self.text = text
        self.words = words if words is not None else []
        self.utterances = utterances if utterances is not None else []

class DiarizedUtterance:
    """Represents a single utterance with speaker label and text."""
    def __init__(self, speaker: str, text: str, start: Optional[int] = None, end: Optional[int] = None):
        self.speaker = speaker
        self.text = text
        self.start = start
        self.end = end

class TimestampedWord:
    """Represents a single word with its text and timestamps."""
    def __init__(self, text: str, start: int, end: int):
        self.text = text
        self.start = start
        self.end = end

if __name__ == "__main__":
    # Example usage
    # job = TranscriptionJob("abc-123", "completed")
    # print(f"Job ID: {job.job_id}, Status: {job.status}")

    # result = TranscriptionResult(
    #     text="Hello world.",
    #     words=[{"text": "Hello", "start": 0, "end": 500}, {"text": "world.", "start": 500, "end": 1000}],
    #     utterances=[{"speaker": "A", "text": "Hello world.", "start": 0, "end": 1000}]
    # )
    # print(f"Result text: {result.text}")
    pass