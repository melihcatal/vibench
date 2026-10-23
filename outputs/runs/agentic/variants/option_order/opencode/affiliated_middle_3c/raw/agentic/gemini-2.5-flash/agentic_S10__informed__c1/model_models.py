import dataclasses
import json
from typing import Any, Dict, List, Optional


@dataclasses.dataclass
class LLMRequest:
    prompt: str
    model: str = "gemini-pro"
    temperature: float = 0.7
    max_tokens: int = 1024


@dataclasses.dataclass
class LLMContextRequest(LLMRequest):
    context: str
    question: str


@dataclasses.dataclass
class LLMResponse:
    text: str
    model: str


@dataclasses.dataclass
class EmbeddingRequest:
    text: List[str]
    model: str = "models/embedding-001"


@dataclasses.dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
    model: str


@dataclasses.dataclass
class SafetyCheckRequest:
    text: str


@dataclasses.dataclass
class SafetyCheckResponse:
    is_safe: bool
    scores: Dict[str, float]


@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclasses.dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str


@dataclasses.dataclass
class TextToSpeechRequest:
    text: str
    language_code: str = "en-US"
    voice_name: str = "en-US-Standard-A"


@dataclasses.dataclass
class TextToSpeechResponse:
    audio_content: bytes


def normalize_json_output(text: str) -> Dict[str, Any]:
    try:
        # Attempt to find the JSON object within the text
        start_idx = text.find("{")
        end_idx = text.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_str = text[start_idx : end_idx + 1]
            return json.loads(json_str)
        else:
            return {"error": "No valid JSON object found in text", "raw_text": text}
    except json.JSONDecodeError as e:
        return {"error": f"JSON decoding failed: {e}", "raw_text": text}
