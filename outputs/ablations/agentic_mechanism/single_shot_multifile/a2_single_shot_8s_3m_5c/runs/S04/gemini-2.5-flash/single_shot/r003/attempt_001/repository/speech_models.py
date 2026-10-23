from typing import Optional, List, Dict, Any

class TranscriptionJobRequest:
    def __init__(self, job_name: str, media_uri: str, language_code: str = "en-US", output_bucket: Optional[str] = None):
        self.job_name = job_name
        self.media_uri = media_uri
        self.language_code = language_code
        self.output_bucket = output_bucket

class TranscriptionJobStatus:
    def __init__(self, job_name: str, status: str, failure_reason: Optional[str] = None, transcript_uri: Optional[str] = None):
        self.job_name = job_name
        self.status = status
        self.failure_reason = failure_reason
        self.transcript_uri = transcript_uri

class TranscriptResult:
    def __init__(self, full_text: str, items: List[Dict[str, Any]], segments: Optional[List[Dict[str, Any]]] = None):
        self.full_text = full_text
        self.items = items # Raw items from AWS Transcribe result, includes word-level details
        self.segments = segments # Optional, might contain segment data if available (e.g., from subtitles)
