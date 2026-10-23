from typing import Dict, Any, List


class LLMRequest:
    def __init__(self, prompt: str, model_id: str, max_tokens: int = 1024):
        self.prompt = prompt
        self.model_id = model_id
        self.max_tokens = max_tokens


class LLMResponse:
    def __init__(self, text: str):
        self.text = text


class JSONExtractionResponse:
    def __init__(self, json_output: Dict[str, Any]):
        self.json_output = json_output


class ContextualAnswerResponse:
    def __init__(self, answer: str):
        self.answer = answer


class EmbeddingRequest:
    def __init__(self, text: str):
        self.text = text


class EmbeddingResponse:
    def __init__(self, embedding: List[float]):
        self.embedding = embedding


class SafetyCheckRequest:
    def __init__(self, text: str):
        self.text = text


class SafetyCheckResponse:
    def __init__(self, is_safe: bool, reasons: List[str]):
        self.is_safe = is_safe
        self.reasons = reasons


class TranslateRequest:
    def __init__(self, text: str, source_language: str, target_language: str):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language


class TranslateResponse:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text


class SpokenBriefRequest:
    def __init__(self, text: str, voice_id: str = "Joanna"):
        self.text = text
        self.voice_id = voice_id


class SpokenBriefResponse:
    def __init__(self, audio_content: bytes):
        self.audio_content = audio_content
