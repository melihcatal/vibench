from typing import List, Dict, Any, Optional

class TranscriptionJob:
    def __init__(self, job_id: str, status: str, transcript_uri: Optional[str] = None):
        self.job_id = job_id
        self.status = status
        self.transcript_uri = transcript_uri

class TranscriptSegment:
    def __init__(self, start_time: float, end_time: float, speaker_label: str, content: str, words: Optional[List[Dict[str, Any]]] = None):
        self.start_time = start_time
        self.end_time = end_time
        self.speaker_label = speaker_label
        self.content = content
        self.words = words

class TranscriptionResult:
    def __init__(self, job_id: str, status: str, language_code: str, segments: List[TranscriptSegment]):
        self.job_id = job_id
        self.status = status
        self.language_code = language_code
        self.segments = segments
