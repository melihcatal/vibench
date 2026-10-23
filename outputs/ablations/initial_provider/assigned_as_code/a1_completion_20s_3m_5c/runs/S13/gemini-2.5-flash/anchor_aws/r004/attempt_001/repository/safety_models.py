from typing import List, Dict, Any

class TextModerationRequest:
    text: str
    language_code: str = "en"

class BatchTextModerationRequest:
    texts: List[str]
    language_code: str = "en"

class TextModerationResult:
    text: str
    is_safe: bool
    scores: Dict[str, float]
    categories: List[Dict[str, Any]]

class RedactionResult:
    original_text: str
    redacted_text: str
    detections: List[Dict[str, Any]]

class ModerationDecision:
    text: str
    allowed: bool
    reasons: List[str]

class SummarizationRequest:
    text_to_summarize: str

class SummarizationResult:
    summary: str

class TranslationRequest:
    text_to_translate: str
    source_language: str
    target_language: str

class TranslationResult:
    translated_text: str

class EmbeddingRequest:
    text_to_embed: str

class EmbeddingResult:
    embedding: List[float]

class AudioGenerationRequest:
    text_to_speak: str
    voice_id: str = "Joanna"
    output_format: str = "mp3"

class AudioGenerationResult:
    audio_content: bytes
