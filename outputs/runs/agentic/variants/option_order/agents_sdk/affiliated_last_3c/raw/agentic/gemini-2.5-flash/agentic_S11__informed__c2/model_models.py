from typing import Dict, Any, List, Optional

class ModelRequest:
    """Represents a standardized request to a generative model."""
    def __init__(self, prompt: str, model_id: Optional[str] = None, parameters: Optional[Dict[str, Any]] = None):
        self.prompt = prompt
        self.model_id = model_id
        self.parameters = parameters if parameters is not None else {}

class ModelResponse:
    """Represents a standardized response from a generative model."""
    def __init__(self, text: str, model_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        self.text = text
        self.model_id = model_id
        self.metadata = metadata if metadata is not None else {}

class SafetyCheckResult:
    """Represents the result of a content safety check."""
    def __init__(self, is_safe: bool, categories: Optional[Dict[str, str]] = None, raw_response: Optional[Dict[str, Any]] = None):
        self.is_safe = is_safe
        self.categories = categories if categories is not None else {}
        self.raw_response = raw_response if raw_response is not None else {}

class TranslationResult:
    """Represents the result of a translation operation."""
    def __init__(self, translated_text: str, source_language: Optional[str] = None, target_language: Optional[str] = None, raw_response: Optional[Dict[str, Any]] = None):
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language
        self.raw_response = raw_response if raw_response is not None else {}

class EmbeddingResult:
    """Represents the result of an embedding operation."""
    def __init__(self, embeddings: List[List[float]], raw_response: Optional[Dict[str, Any]] = None):
        self.embeddings = embeddings
        self.raw_response = raw_response if raw_response is not None else {}

class AudioBriefingResult:
    """Represents the result of an audio briefing generation."""
    def __init__(self, audio_content: bytes, audio_format: str, raw_response: Optional[Dict[str, Any]] = None):
        self.audio_content = audio_content
        self.audio_format = audio_format
        self.raw_response = raw_response if raw_response is not None else {}
