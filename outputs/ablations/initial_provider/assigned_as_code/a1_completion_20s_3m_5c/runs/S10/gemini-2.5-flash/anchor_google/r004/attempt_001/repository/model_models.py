from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class LLMRequest:
    text: str
    model: str = "gemini-2.5-flash"
    temperature: float = 0.7
    max_output_tokens: int = 1024

@dataclass
class LLMResponse:
    text: str

@dataclass
class ContextualLLMRequest(LLMRequest):
    context: str
    question: str

@dataclass
class JsonExtractionLLMRequest(LLMRequest):
    format_instructions: str

@dataclass
class SafetyCheckRequest:
    text: str

@dataclass
class TranslateRequest:
    text: str
    target_language_code: str
    source_language_code: str = "en"

@dataclass
class EmbeddingRequest:
    text: List[str]
    model: str = "text-embedding-004"

@dataclass
class SpokenBriefRequest:
    text: str
    language_code: str = "en-US"
    voice_name: str = "en-US-Standard-A"
