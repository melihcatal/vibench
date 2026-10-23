from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class TranscriptionPayload(BaseModel):
    audio_uri: str
    language_code: str
    display_name: Optional[str] = "transcription"
    diarization_enabled: Optional[bool] = False
    word_level_timestamps_enabled: Optional[bool] = False

class TranscriptionConfig(BaseModel):
    api_key: Optional[str] = None
    region: str = "eastus"
    job_name: Optional[str] = "transcription"

class TranscriptionJob(BaseModel):
    job_id: str
    status: str
    result_uri: Optional[str] = None

class TranscriptionResultWord(BaseModel):
    word: str
    offset: str
    duration: str

class TranscriptionResultSegment(BaseModel):
    text: str
    speaker: Optional[int] = None
    words: Optional[List[TranscriptionResultWord]] = None

class TranscriptionResult(BaseModel):
    duration: str
    combinedRecognizedPhrases: Optional[List[Dict[str, Any]]] = None
    recognizedPhrases: Optional[List[Dict[str, Any]]] = None

class TranslationPayload(BaseModel):
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None

class ModerationPayload(BaseModel):
    text: str

class SummarizationPayload(BaseModel):
    text: str

class EmbeddingPayload(BaseModel):
    text_segments: List[str]
