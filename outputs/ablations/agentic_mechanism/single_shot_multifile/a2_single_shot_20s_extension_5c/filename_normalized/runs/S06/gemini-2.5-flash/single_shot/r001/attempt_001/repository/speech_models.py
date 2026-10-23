from pydantic import BaseModel
from typing import List, Optional

class SynthesisRequest(BaseModel):
    text: str
    voice_id: str
    output_format: str = "mp3"

class SSMLSynthesisRequest(BaseModel):
    ssml_text: str
    voice_id: str
    output_format: str = "mp3"

class Voice(BaseModel):
    id: str
    name: str
    language_code: str

class TranslationRequest(BaseModel):
    text: str
    source_language_code: str
    target_language_code: str

class SafetyCheckRequest(BaseModel):
    text: str
    language_code: str = "en"

class EmbeddingRequest(BaseModel):
    text: str
    model: str = "text-embedding-3-small"

class TranscriptionRequest(BaseModel):
    audio_file_uri: str 
    output_bucket_name: str
    job_name: str
    language_code: str = "en-US"
    media_format: str = "mp3"
