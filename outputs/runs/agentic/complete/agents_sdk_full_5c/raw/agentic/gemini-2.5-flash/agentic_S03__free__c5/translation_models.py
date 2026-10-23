from dataclasses import dataclass

@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: str = ""
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id") # Default project_id

@dataclass
class BatchTranslationRequest:
    texts: list[str]
    target_language: str
    source_language: str = ""
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")

@dataclass
class DictionaryTranslationRequest:
    data: dict[str, str]
    target_language: str
    source_language: str = ""
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")

@dataclass
class TranslationResponse:
    translated_text: str

@dataclass
class TextToSummarize:
    text: str

@dataclass
class SummaryResponse:
    summary: str

@dataclass
class ContentCheckRequest:
    text: str

@dataclass
class ContentCheckResponse:
    is_unsafe: bool
    details: str

@dataclass
class EmbeddingRequest:
    text: str

@dataclass
class EmbeddingResponse:
    embedding: list[float]

@dataclass
class AudioPreviewRequest:
    text: str
    language_code: str
    voice_name: str

@dataclass
class AudioPreviewResponse:
    audio_content: bytes
