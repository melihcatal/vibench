from dataclasses import dataclass
from typing import List, Dict

@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: str
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    location: str = "global"

@dataclass
class TranslationResponse:
    translated_text: str

@dataclass
class BatchTranslationRequest:
    texts: List[str]
    target_language: str
    source_language: str
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    location: str = "global"

@dataclass
class BatchTranslationResponse:
    translated_texts: List[str]

@dataclass
class DictionaryTranslationRequest:
    dictionary_data: Dict[str, str]
    target_language: str
    source_language: str
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    location: str = "global"

@dataclass
class DictionaryTranslationResponse:
    translated_dictionary: Dict[str, str]

@dataclass
class QualitySummaryRequest:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str

@dataclass
class QualitySummaryResponse:
    summary: str

@dataclass
class UnsafeContentCheckRequest:
    text: str
    language: str

@dataclass
class UnsafeContentCheckResponse:
    is_unsafe: bool
    categories: List[str]

@dataclass
class EmbeddingRequest:
    text_segments: List[str]

@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]

@dataclass
class AudioPreviewRequest:
    text: str
    language_code: str
    voice_name: str
    audio_encoding: str = "LINEAR16" # MP3, LINEAR16, OGG_OPUS

@dataclass
class AudioPreviewResponse:
    audio_content: bytes
