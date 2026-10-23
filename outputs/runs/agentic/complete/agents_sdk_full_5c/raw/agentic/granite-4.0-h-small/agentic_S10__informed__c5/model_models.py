from typing import Any, Dict, List, TypedDict

# Request/response model representations used internally by the same-scenario files

class LLMChatMessage(TypedDict):
    role: str  # "system", "user", or "assistant"
    content: str

# Normalized response from any provider (convert to common shape for downstream steps)

class NormalizedLLMResponse(TypedDict):
    choices: List[Dict[str, Any]]  # At least one choice with a message field

# Simple safety flag for prompt generation (used by prompt_safety.py)

class SafetyCheckResult(TypedDict):
    safe: bool
    flagged_content: List[str]  # optional list of detected unsafe fragments

# Basic translation result

class TranslationResult(TypedDict):
    translated_text: str

# Embedding result (single vector list)

class EmbeddingResult(TypedDict):
    embedding: List[float]

# Text-to-speech synthesis result (audio buffer or URI)

class TTSResult(TypedDict):
    audio_url: str
    duration_seconds: float
